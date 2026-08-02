#!/usr/bin/env bash
set -euo pipefail

# Rebuild the historical PX4/ROS 2/Gazebo Classic validation environment.
# Run as root inside an isolated Ubuntu 22.04 WSL distribution.

TARGET_USER="${TARGET_USER:-paneendra}"
PX4_REF="${PX4_REF:-v1.14.4}"
PX4_MSGS_REF="${PX4_MSGS_REF:-release/1.14}"
XRCE_AGENT_REF="${XRCE_AGENT_REF:-v2.4.3}"
PROJECT_REPOSITORY="${PROJECT_REPOSITORY:-https://github.com/paneendrakumar0/uav-autonomous-telemetry.git}"

if [[ "${EUID}" -ne 0 ]]; then
  echo "Run this script as root inside Ubuntu 22.04." >&2
  exit 1
fi

if [[ "$(. /etc/os-release && printf '%s' "${VERSION_ID}")" != "22.04" ]]; then
  echo "This bootstrap is intentionally restricted to Ubuntu 22.04." >&2
  exit 1
fi

printf '%s\n' \
  'Acquire::ForceIPv4 "true";' \
  'Acquire::Retries "10";' \
  'Acquire::http::Timeout "60";' \
  'Acquire::https::Timeout "60";' \
  > /etc/apt/apt.conf.d/99-validation-network

if ! id "${TARGET_USER}" >/dev/null 2>&1; then
  useradd --create-home --shell /bin/bash "${TARGET_USER}"
fi

apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y \
  ca-certificates \
  curl \
  gnupg \
  locales \
  software-properties-common \
  sudo

locale-gen en_US en_US.UTF-8
update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
add-apt-repository universe -y

install -d -m 0755 /usr/share/keyrings
if [[ ! -s /usr/share/keyrings/ros-archive-keyring.gpg ]]; then
  curl -fsSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
    -o /usr/share/keyrings/ros-archive-keyring.gpg
fi
printf '%s\n' \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu jammy main" \
  > /etc/apt/sources.list.d/ros2.list

apt-get update
DEBIAN_FRONTEND=noninteractive apt-get upgrade -y
DEBIAN_FRONTEND=noninteractive apt-get install -y \
  astyle \
  bc \
  build-essential \
  cmake \
  gazebo \
  git \
  libeigen3-dev \
  libgazebo-dev \
  libgstreamer1.0-dev \
  libgstreamer-plugins-base1.0-dev \
  libopencv-dev \
  libxml2-dev \
  libxml2-utils \
  ninja-build \
  pkg-config \
  protobuf-compiler \
  python3-dev \
  python3-pip \
  python3-setuptools \
  python3-venv \
  python3-wheel \
  ros-dev-tools \
  ros-humble-ros-base \
  rsync \
  unzip \
  zip

usermod -aG sudo "${TARGET_USER}"
printf '%s\n' "${TARGET_USER} ALL=(ALL) NOPASSWD:ALL" \
  > "/etc/sudoers.d/${TARGET_USER}-wsl"
chmod 0440 "/etc/sudoers.d/${TARGET_USER}-wsl"

user_home="$(getent passwd "${TARGET_USER}" | cut -d: -f6)"

run_as_user() {
  sudo -H -u "${TARGET_USER}" env \
    PATH="${user_home}/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
    bash -lc "$1"
}

run_as_user "
  if [[ ! -d \"${user_home}/PX4-Autopilot/.git\" ]]; then
    git clone --branch \"${PX4_REF}\" --depth 1 --recurse-submodules --shallow-submodules \
      https://github.com/PX4/PX4-Autopilot.git \"${user_home}/PX4-Autopilot\"
  fi
  # PX4 v1.14's version-header generator requires at least one NuttX release
  # tag, which shallow submodule clones do not include.
  if ! git -C \"${user_home}/PX4-Autopilot/platforms/nuttx/NuttX/nuttx\" \
      tag --list nuttx-11.0.0 | grep -qx nuttx-11.0.0; then
    git -C \"${user_home}/PX4-Autopilot/platforms/nuttx/NuttX/nuttx\" \
      fetch --depth 1 origin tag nuttx-11.0.0
  fi
"

# PX4's Ubuntu 22.04 setup defaults to modern Gazebo, while this project needs
# Gazebo Classic. Install only PX4's common build dependencies here.
run_as_user "
  cd \"${user_home}/PX4-Autopilot\"
  bash Tools/setup/ubuntu.sh --no-nuttx --no-sim-tools
"

run_as_user "
  if [[ ! -d \"${user_home}/Micro-XRCE-DDS-Agent/.git\" ]]; then
    git clone --branch \"${XRCE_AGENT_REF}\" --depth 1 --recurse-submodules \
      https://github.com/eProsima/Micro-XRCE-DDS-Agent.git \
      \"${user_home}/Micro-XRCE-DDS-Agent\"
  fi
  cmake -S \"${user_home}/Micro-XRCE-DDS-Agent\" \
    -B \"${user_home}/Micro-XRCE-DDS-Agent/build\" \
    -DCMAKE_BUILD_TYPE=Release
  cmake --build \"${user_home}/Micro-XRCE-DDS-Agent/build\" --parallel 2
"
cmake --install "${user_home}/Micro-XRCE-DDS-Agent/build"
ldconfig

run_as_user "
  if [[ ! -d \"${user_home}/uav-autonomous-telemetry/.git\" ]]; then
    git clone --depth 1 \"${PROJECT_REPOSITORY}\" \"${user_home}/uav-autonomous-telemetry\"
  fi
  mkdir -p \"${user_home}/px4_msgs_ws/src\"
  if [[ ! -d \"${user_home}/px4_msgs_ws/src/px4_msgs/.git\" ]]; then
    git clone --branch \"${PX4_MSGS_REF}\" --depth 1 \
      https://github.com/PX4/px4_msgs.git \
      \"${user_home}/px4_msgs_ws/src/px4_msgs\"
  fi
  python3 -m pip install --user \
    -r \"${user_home}/uav-autonomous-telemetry/requirements-analysis.txt\"
  chmod 0755 \
    \"${user_home}/uav-autonomous-telemetry/ros2_ws/src/uav_control/scripts/payload_swing_logger\"
"

repo_root="${user_home}/uav-autonomous-telemetry"
px4_root="${user_home}/PX4-Autopilot"
install -m 0644 \
  "${repo_root}/px4_payload_integration/ROMFS/px4fmu_common/init.d-posix/airframes/1020_gazebo-classic_iris_depth_payload" \
  "${px4_root}/ROMFS/px4fmu_common/init.d-posix/airframes/"
install -m 0644 \
  "${repo_root}/px4_payload_integration/ROMFS/px4fmu_common/init.d-posix/airframes/CMakeLists.txt" \
  "${px4_root}/ROMFS/px4fmu_common/init.d-posix/airframes/CMakeLists.txt"
install -m 0644 \
  "${repo_root}/px4_payload_integration/src/modules/simulation/simulator_mavlink/sitl_targets_gazebo-classic.cmake" \
  "${px4_root}/src/modules/simulation/simulator_mavlink/sitl_targets_gazebo-classic.cmake"
install -d \
  "${px4_root}/Tools/simulation/gazebo-classic/sitl_gazebo-classic/models/iris_depth_payload"
install -m 0644 \
  "${repo_root}/px4_payload_integration/Tools/simulation/gazebo-classic/sitl_gazebo-classic/models/iris_depth_payload/"* \
  "${px4_root}/Tools/simulation/gazebo-classic/sitl_gazebo-classic/models/iris_depth_payload/"
chown -R "${TARGET_USER}:${TARGET_USER}" \
  "${px4_root}" \
  "${user_home}/px4_msgs_ws" \
  "${user_home}/uav-autonomous-telemetry"

run_as_user "
  cd \"${px4_root}\"
  make px4_sitl_default -j2
  ninja -C build/px4_sitl_default sitl_gazebo-classic
  cd \"${user_home}/px4_msgs_ws\"
  source /opt/ros/humble/setup.bash
  colcon build --symlink-install
  source \"${user_home}/px4_msgs_ws/install/setup.bash\"
  cd \"${repo_root}/ros2_ws\"
  colcon build --symlink-install
"

grep -qxF "source /opt/ros/humble/setup.bash" "${user_home}/.bashrc" ||
  printf '%s\n' "source /opt/ros/humble/setup.bash" >> "${user_home}/.bashrc"
grep -qxF "source ~/px4_msgs_ws/install/setup.bash" "${user_home}/.bashrc" ||
  printf '%s\n' "source ~/px4_msgs_ws/install/setup.bash" >> "${user_home}/.bashrc"
grep -qxF "source ~/uav-autonomous-telemetry/ros2_ws/install/setup.bash" "${user_home}/.bashrc" ||
  printf '%s\n' "source ~/uav-autonomous-telemetry/ros2_ws/install/setup.bash" >> "${user_home}/.bashrc"
chown "${TARGET_USER}:${TARGET_USER}" "${user_home}/.bashrc"

cat > /etc/wsl.conf <<EOF
[user]
default=${TARGET_USER}
EOF

printf '\nEnvironment installation complete.\n'
printf 'PX4: %s\n' "${PX4_REF}"
printf 'px4_msgs: %s\n' "${PX4_MSGS_REF}"
printf 'Micro XRCE-DDS Agent: %s\n' "${XRCE_AGENT_REF}"
printf 'Project: %s\n' "${repo_root}"
