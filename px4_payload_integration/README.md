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

Current status: the payload target boots, accepts PX4 offboard arming, and hovers correctly with a native internal `base_link -> slung_payload` ball joint. The working baseline removes payload collision geometry to avoid ground-contact solver locking at spawn, while preserving payload mass, cable visual, payload visual, and the pose-sniffer logger.

The pose-sniffer plugin now tracks both `base_link` and `slung_payload`. This lets `payload_swing_logger` compute cable length, lateral swing, and cable angle from a same-frame Gazebo link pair instead of mixing Gazebo payload pose with PX4 local-position estimates.
