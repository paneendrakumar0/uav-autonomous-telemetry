# ==============================================================================
# UAV Slung-Payload SITL — Reproducible Docker Environment
# ==============================================================================
# This Dockerfile satisfies the reproducibility requirements by pinning all
# major dependencies to specific versions:
# - ROS 2: Humble Hawksbill
# - Gazebo: Classic 11
# - PX4 Autopilot: v1.15.2
# - Micro XRCE-DDS Agent: v2.4.2
# - px4_msgs: release/1.15
# ==============================================================================

FROM osrf/ros:humble-desktop

ENV DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-c"]

# ------------------------------------------------------------------------------
# 1. System Dependencies & Gazebo Classic 11
# ------------------------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends wget gnupg lsb-release && \ 
    wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg && \ 
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable jammy main" | tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null && \ 
    apt-get update && apt-get install -y --no-install-recommends \
    gazebo \
    libgazebo11-dev \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-octomap \
    ros-humble-octomap-msgs \
    ros-humble-octomap-server \
    python3-pyqt6 \
    python3-pyqtgraph \
    git \
    wget \
    curl \
    cmake \
    build-essential \
    ninja-build \
    python3-pip \
    python3-jinja2 \
    python3-empy \
    python3-toml \
    python3-numpy \
    python3-packaging \
    python3-jsonschema \
    python3-setuptools \
    python3-cerberus \
    python3-coverage \
    python3-requests \
    python3-future \
    python3-pandas \
    python3-matplotlib \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-libav \
    gstreamer1.0-gl \
    libgstreamer-plugins-base1.0-dev \
    libimage-exiftool-perl \
    astyle \
    xmlstarlet \
    protobuf-compiler \
    libeigen3-dev \
    libopencv-dev \
    libxml2-utils \
    unzip \
    xxd \
    dmidecode \
    bc \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir kconfiglib pyros-genmsg pyulog

WORKDIR /root

# ------------------------------------------------------------------------------
# 2. PX4 Autopilot (Pinned to v1.15.2)
# ------------------------------------------------------------------------------
ARG PX4_TAG=v1.15.2
RUN git clone --recursive --branch ${PX4_TAG} https://github.com/PX4/PX4-Autopilot.git && \
    cd PX4-Autopilot && \
    bash ./Tools/setup/ubuntu.sh --no-sim-tools --no-nuttx && \
    make px4_sitl_default -j$(nproc)

# ------------------------------------------------------------------------------
# 3. Micro XRCE-DDS Agent (Pinned to v2.4.2)
# ------------------------------------------------------------------------------
ARG DDS_AGENT_TAG=v2.4.2
RUN git clone --depth 1 --branch ${DDS_AGENT_TAG} https://github.com/eProsima/Micro-XRCE-DDS-Agent.git && \
    cd Micro-XRCE-DDS-Agent && \
    mkdir build && cd build && \
    cmake .. && \
    make -j$(nproc) && \
    make install && \
    ldconfig

# ------------------------------------------------------------------------------
# 4. px4_msgs ROS 2 Workspace (Pinned to release/1.15)
# ------------------------------------------------------------------------------
RUN mkdir -p /root/px4_msgs_ws/src && \
    git clone --depth 1 --branch release/1.15 https://github.com/PX4/px4_msgs.git /root/px4_msgs_ws/src/px4_msgs && \
    cd /root/px4_msgs_ws && \
    source /opt/ros/humble/setup.bash && \
    colcon build --packages-select px4_msgs --symlink-install

# ------------------------------------------------------------------------------
# 5. Inject Repository Source & Payload Models
# ------------------------------------------------------------------------------
COPY ros2_ws/src/uav_control  /root/ros2_ws/src/uav_control
COPY px4_payload_integration  /root/px4_payload_integration
COPY tools                    /root/uav-autonomous-telemetry/tools
COPY requirements-analysis.txt /root/uav-autonomous-telemetry/

# Apply PX4 payload integration files (Airframes, SDF models, CMake, Worlds)
RUN PX4=/root/PX4-Autopilot && \
    cp /root/px4_payload_integration/ROMFS/px4fmu_common/init.d-posix/airframes/1020_gazebo-classic_iris_depth_payload \
       "${PX4}/ROMFS/px4fmu_common/init.d-posix/airframes/" && \
    cp /root/px4_payload_integration/ROMFS/px4fmu_common/init.d-posix/airframes/CMakeLists.txt \
       "${PX4}/ROMFS/px4fmu_common/init.d-posix/airframes/CMakeLists.txt" && \
    cp /root/px4_payload_integration/src/modules/simulation/simulator_mavlink/sitl_targets_gazebo-classic.cmake \
       "${PX4}/src/modules/simulation/simulator_mavlink/sitl_targets_gazebo-classic.cmake" && \
    mkdir -p "${PX4}/Tools/simulation/gazebo-classic/sitl_gazebo-classic/models/iris_depth_payload" && \
    cp /root/px4_payload_integration/Tools/simulation/gazebo-classic/sitl_gazebo-classic/models/iris_depth_payload/* \
       "${PX4}/Tools/simulation/gazebo-classic/sitl_gazebo-classic/models/iris_depth_payload/" && \
    mkdir -p "${PX4}/Tools/simulation/gazebo-classic/sitl_gazebo-classic/models/ros2_depth_camera" && \
    cp /root/px4_payload_integration/Tools/simulation/gazebo-classic/sitl_gazebo-classic/models/ros2_depth_camera/* \
       "${PX4}/Tools/simulation/gazebo-classic/sitl_gazebo-classic/models/ros2_depth_camera/" && \
    cp /root/px4_payload_integration/Tools/simulation/gazebo-classic/sitl_gazebo-classic/worlds/*.world \
       "${PX4}/Tools/simulation/gazebo-classic/sitl_gazebo-classic/worlds/" 2>/dev/null || true && \
    cd "${PX4}" && make px4_sitl_default -j$(nproc)

# ------------------------------------------------------------------------------
# 6. Build Project ROS 2 Workspace
# ------------------------------------------------------------------------------
RUN cd /root/ros2_ws && \
    source /opt/ros/humble/setup.bash && \
    source /root/px4_msgs_ws/install/setup.bash && \
    colcon build --packages-select uav_control

# ------------------------------------------------------------------------------
# 7. Environment Setup
# ------------------------------------------------------------------------------
RUN { \
      echo '# --- UAV Slung-Payload SITL Environment ---'; \
      echo 'source /opt/ros/humble/setup.bash'; \
      echo 'source /root/px4_msgs_ws/install/setup.bash'; \
      echo 'source /root/ros2_ws/install/setup.bash'; \
      echo 'export PX4_HOME=/root/PX4-Autopilot'; \
    } >> /root/.bashrc

# Set working directory to project tools for easy experiment running
WORKDIR /root/uav-autonomous-telemetry
CMD ["/bin/bash"]
