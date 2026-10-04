# ============================================================
# UAV Slung-Payload SITL — Reproducible Environment
# ============================================================
# Build:   docker build -t uav-payload-sitl .
# Run:     docker run -it --rm uav-payload-sitl
# ============================================================
FROM osrf/ros:humble-desktop

ENV DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-c"]

# ── 1. System dependencies ───────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    # --- Gazebo Classic 11 ---
    gazebo \
    libgazebo11-dev \
    ros-humble-gazebo-ros-pkgs \
    # --- Build tools ---
    git \
    wget \
    curl \
    cmake \
    build-essential \
    ninja-build \
    # --- PX4 build dependencies ---
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
    # --- Analysis / plotting ---
    python3-pandas \
    python3-matplotlib \
    # --- GStreamer (PX4 SITL video pipeline) ---
    gstreamer1.0-plugins-bad \
    gstreamer1.0-libav \
    gstreamer1.0-gl \
    libgstreamer-plugins-base1.0-dev \
    # --- Misc PX4 / SITL deps ---
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

# Python packages required by PX4 build system
RUN pip3 install --no-cache-dir \
    kconfiglib \
    pyros-genmsg \
    pyulog

WORKDIR /root

# ── 2. PX4-Autopilot (pinned to stable release) ─────────────
# Pin to a known Gazebo-Classic-compatible stable tag.
# Change PX4_TAG if your local setup uses a different version.
ARG PX4_TAG=v1.15.2
RUN git clone --recursive --branch ${PX4_TAG} \
      https://github.com/PX4/PX4-Autopilot.git && \
    cd PX4-Autopilot && \
    bash ./Tools/setup/ubuntu.sh --no-sim-tools --no-nuttx && \
    make px4_sitl_default -j$(nproc)

# ── 3. Micro-XRCE-DDS-Agent ─────────────────────────────────
ARG DDS_AGENT_TAG=v2.4.2
RUN git clone --depth 1 --branch ${DDS_AGENT_TAG} \
      https://github.com/eProsima/Micro-XRCE-DDS-Agent.git && \
    cd Micro-XRCE-DDS-Agent && \
    mkdir build && cd build && \
    cmake .. && \
    make -j$(nproc) && \
    make install && \
    ldconfig

# ── 4. px4_msgs ROS 2 workspace ─────────────────────────────
RUN mkdir -p /root/px4_msgs_ws/src && \
    git clone --depth 1 --branch release/1.15 \
      https://github.com/PX4/px4_msgs.git /root/px4_msgs_ws/src/px4_msgs && \
    cd /root/px4_msgs_ws && \
    source /opt/ros/humble/setup.bash && \
    colcon build --packages-select px4_msgs --symlink-install

# ── 5. Copy project source into the image ────────────────────
COPY ros2_ws/src/uav_control  /root/ros2_ws/src/uav_control
COPY px4_payload_integration  /root/px4_payload_integration
COPY tools                    /root/uav-autonomous-telemetry/tools
COPY requirements-analysis.txt /root/uav-autonomous-telemetry/

# ── 6. Apply PX4 payload integration files ───────────────────
RUN PX4=/root/PX4-Autopilot && \
    # Airframe
    cp /root/px4_payload_integration/ROMFS/px4fmu_common/init.d-posix/airframes/1020_gazebo-classic_iris_depth_payload \
       "${PX4}/ROMFS/px4fmu_common/init.d-posix/airframes/" && \
    cp /root/px4_payload_integration/ROMFS/px4fmu_common/init.d-posix/airframes/CMakeLists.txt \
       "${PX4}/ROMFS/px4fmu_common/init.d-posix/airframes/CMakeLists.txt" && \
    # SITL cmake target
    cp /root/px4_payload_integration/src/modules/simulation/simulator_mavlink/sitl_targets_gazebo-classic.cmake \
       "${PX4}/src/modules/simulation/simulator_mavlink/sitl_targets_gazebo-classic.cmake" && \
    # Payload Gazebo model
    mkdir -p "${PX4}/Tools/simulation/gazebo-classic/sitl_gazebo-classic/models/iris_depth_payload" && \
    cp /root/px4_payload_integration/Tools/simulation/gazebo-classic/sitl_gazebo-classic/models/iris_depth_payload/* \
       "${PX4}/Tools/simulation/gazebo-classic/sitl_gazebo-classic/models/iris_depth_payload/" && \
    # Wind disturbance world files
    cp /root/px4_payload_integration/Tools/simulation/gazebo-classic/sitl_gazebo-classic/worlds/*.world \
       "${PX4}/Tools/simulation/gazebo-classic/sitl_gazebo-classic/worlds/" 2>/dev/null || true && \
    # Rebuild PX4 with payload target
    cd "${PX4}" && make px4_sitl_default -j$(nproc)

# ── 7. Build uav_control ROS 2 workspace ────────────────────
RUN cd /root/ros2_ws && \
    source /opt/ros/humble/setup.bash && \
    source /root/px4_msgs_ws/install/setup.bash && \
    colcon build --packages-select uav_control

# ── 8. Shell environment — sources everything on login ───────
RUN { \
      echo '# --- UAV Slung-Payload SITL environment ---'; \
      echo 'source /opt/ros/humble/setup.bash'; \
      echo 'source /root/px4_msgs_ws/install/setup.bash'; \
      echo 'source /root/ros2_ws/install/setup.bash'; \
      echo 'export PX4_HOME=/root/PX4-Autopilot'; \
    } >> /root/.bashrc

CMD ["/bin/bash"]
