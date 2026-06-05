# PX4 Payload Integration Files

This directory mirrors the PX4-Autopilot relative paths for the current slung-payload Gazebo Classic integration.

Copy these files into a PX4-Autopilot checkout, then rebuild `px4_sitl_default`.

```bash
PX4_DIR=~/PX4-Autopilot

cp ROMFS/px4fmu_common/init.d-posix/airframes/1020_gazebo-classic_iris_depth_payload \
  "$PX4_DIR/ROMFS/px4fmu_common/init.d-posix/airframes/"

cp ROMFS/px4fmu_common/init.d-posix/airframes/CMakeLists.txt \
  "$PX4_DIR/ROMFS/px4fmu_common/init.d-posix/airframes/CMakeLists.txt"

cp src/modules/simulation/simulator_mavlink/sitl_targets_gazebo-classic.cmake \
  "$PX4_DIR/src/modules/simulation/simulator_mavlink/sitl_targets_gazebo-classic.cmake"

mkdir -p "$PX4_DIR/Tools/simulation/gazebo-classic/sitl_gazebo-classic/models/iris_depth_payload"
cp Tools/simulation/gazebo-classic/sitl_gazebo-classic/models/iris_depth_payload/* \
  "$PX4_DIR/Tools/simulation/gazebo-classic/sitl_gazebo-classic/models/iris_depth_payload/"

cd "$PX4_DIR"
make px4_sitl_default -j2
HEADLESS=1 make px4_sitl gazebo-classic_iris_depth_payload
```

Current status: the payload target boots and accepts PX4 offboard arming, and the slung payload is visible in Gazebo. Hover validation still shows that the vehicle remains near ground level, including with the simplified single-link pendulum baseline. The next required correction is the Gazebo Classic payload joint/frame physics before payload hover or payload figure-8 can be claimed as complete.
