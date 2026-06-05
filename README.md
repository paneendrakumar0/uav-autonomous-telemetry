# UAV Autonomous Telemetry and Slung-Payload SITL Experiments

ROS 2 + PX4 SITL workspace for autonomous UAV offboard control, telemetry logging, figure-8 trajectory validation, and early slung-payload simulation in Gazebo Classic.

This repository captures the current project state, including runnable ROS 2 nodes, PX4/Gazebo payload integration files, generated CSV logs, and plot-based experiment reports.

## Project Status

| Stage | Status | Evidence |
| --- | --- | --- |
| PX4 SITL + Gazebo Classic depth-camera vehicle | Complete | `iris_depth_camera` boots and publishes depth/pointcloud topics |
| ROS 2 offboard control bridge | Complete | MicroXRCEAgent and `/fmu/in/*`, `/fmu/out/*` topics verified |
| Continuous figure-8 trajectory without payload | Complete | Tuned run: post-takeoff mean error `0.415 m`, RMS `0.442 m` |
| Telemetry and plotting pipeline | Complete | CSV logs plus XY, XYZ-time, 3D, and error plots generated |
| Slung-payload model integration | Partial | Payload model boots and arms, but does not climb yet |
| Payload hover validation | Blocked by payload SDF physics | Hover controller works on normal Iris, fails only with payload model |

## Repository Layout

```text
.
|-- README.md
|-- ros2_ws/
|   `-- src/uav_control/
|       |-- src/
|       |   |-- offboard_control.cpp
|       |   |-- telemetry_logger.cpp
|       |   |-- figure8_offboard.cpp
|       |   |-- figure8_metrics_logger.cpp
|       |   `-- hover_offboard.cpp
|       |-- scripts/
|       |   `-- payload_swing_logger
|       `-- launch/
|           |-- figure8_experiment.launch.py
|           |-- figure8_payload_experiment.launch.py
|           `-- payload_hover_experiment.launch.py
|-- px4_payload_integration/
|   `-- ... PX4 files to copy into PX4-Autopilot ...
|-- reports/
|   |-- fig8_run_2026-06-04/
|   |-- fig8_metrics_tuned_2026-06-04/
|   |-- payload_hover_2026-06-05/
|   `-- hover_control_check_2026-06-05/
`-- tools/
    `-- legacy_plot_data.py
```

## System Architecture

- Flight stack: PX4 Autopilot SITL
- Simulator: Gazebo Classic 11
- Vehicle baseline: `iris_depth_camera`
- Payload vehicle under development: `iris_depth_payload`
- Middleware bridge: Micro XRCE-DDS Agent
- Autonomy layer: ROS 2 Humble, C++ nodes plus Python logger
- Main telemetry topics:
  - `/fmu/in/offboard_control_mode`
  - `/fmu/in/trajectory_setpoint`
  - `/fmu/in/vehicle_command`
  - `/fmu/out/vehicle_local_position_v1`

## Main ROS 2 Nodes

| Node | File | Purpose |
| --- | --- | --- |
| `offboard_control` | `ros2_ws/src/uav_control/src/offboard_control.cpp` | Original waypoint/offboard control node |
| `telemetry_logger` | `ros2_ws/src/uav_control/src/telemetry_logger.cpp` | Basic telemetry CSV logger |
| `figure8_offboard` | `ros2_ws/src/uav_control/src/figure8_offboard.cpp` | Continuous lemniscate/figure-8 controller |
| `figure8_metrics_logger` | `ros2_ws/src/uav_control/src/figure8_metrics_logger.cpp` | Logs actual vs reference trajectory metrics |
| `hover_offboard` | `ros2_ws/src/uav_control/src/hover_offboard.cpp` | Constant-position hover validation controller |
| `payload_swing_logger` | `ros2_ws/src/uav_control/scripts/payload_swing_logger` | Parses Gazebo pose sniffer UDP packets and logs payload swing estimates |

## Key Results

### 1. Initial Figure-8 SITL Run

The first validated figure-8 run confirmed that PX4 SITL, Gazebo Classic, MicroXRCEAgent, and ROS 2 offboard control were connected end to end.

Artifacts:

- Report: [`reports/fig8_run_2026-06-04/REPORT.md`](reports/fig8_run_2026-06-04/REPORT.md)
- XY plot: [`reports/fig8_run_2026-06-04/figure8_xy.png`](reports/fig8_run_2026-06-04/figure8_xy.png)
- XYZ-time plot: [`reports/fig8_run_2026-06-04/figure8_xyz_vs_time.png`](reports/fig8_run_2026-06-04/figure8_xyz_vs_time.png)
- 3D plot: [`reports/fig8_run_2026-06-04/figure8_3d.png`](reports/fig8_run_2026-06-04/figure8_3d.png)

![Initial figure-8 XY](reports/fig8_run_2026-06-04/figure8_xy.png)

### 2. Tuned Figure-8 Tracking

The slower tuned figure-8 run used `omega=0.25 rad/s` and produced a much cleaner steady-state tracking result.

Artifacts:

- Metrics report: [`reports/fig8_metrics_tuned_2026-06-04/METRICS.md`](reports/fig8_metrics_tuned_2026-06-04/METRICS.md)
- XY comparison: [`reports/fig8_metrics_tuned_2026-06-04/actual_vs_reference_xy.png`](reports/fig8_metrics_tuned_2026-06-04/actual_vs_reference_xy.png)
- Steady-state XY comparison: [`reports/fig8_metrics_tuned_2026-06-04/actual_vs_reference_xy_steady.png`](reports/fig8_metrics_tuned_2026-06-04/actual_vs_reference_xy_steady.png)
- XYZ-time comparison: [`reports/fig8_metrics_tuned_2026-06-04/actual_vs_reference_xyz_time.png`](reports/fig8_metrics_tuned_2026-06-04/actual_vs_reference_xyz_time.png)
- Tracking error: [`reports/fig8_metrics_tuned_2026-06-04/tracking_error_time.png`](reports/fig8_metrics_tuned_2026-06-04/tracking_error_time.png)

Metrics:

| Window | Samples | Mean Error | RMS Error | Max Error |
| --- | ---: | ---: | ---: | ---: |
| Full run | 4305 | `0.839 m` | `1.666 m` | `6.981 m` |
| Post-takeoff, `t >= 12 s` | 3705 | `0.415 m` | `0.442 m` | `0.660 m` |

![Tuned figure-8 XY](reports/fig8_metrics_tuned_2026-06-04/actual_vs_reference_xy_steady.png)

### 3. Slung-Payload Integration Attempt

A Gazebo Classic payload vehicle was added:

- Model: `iris_depth_payload`
- Airframe: `1020_gazebo-classic_iris_depth_payload`
- Payload mass in current lightweight baseline: `0.05 kg`
- Cable link: near-zero mass, 1 m visual cable
- Payload pose logging: Gazebo pose sniffer UDP on `127.0.0.1:7001`

Artifacts:

- Payload status report: [`reports/payload_fig8_light_2026-06-05/PAYLOAD_STATUS_REPORT.md`](reports/payload_fig8_light_2026-06-05/PAYLOAD_STATUS_REPORT.md)
- Payload XY tracking: [`reports/payload_fig8_light_2026-06-05/payload_xy_tracking.png`](reports/payload_fig8_light_2026-06-05/payload_xy_tracking.png)
- Payload XYZ-time: [`reports/payload_fig8_light_2026-06-05/payload_xyz_vs_time.png`](reports/payload_fig8_light_2026-06-05/payload_xyz_vs_time.png)
- Payload cable angle: [`reports/payload_fig8_light_2026-06-05/payload_cable_angle.png`](reports/payload_fig8_light_2026-06-05/payload_cable_angle.png)

Current finding: the payload model boots and PX4 accepts offboard arming, but it does not produce a valid airborne figure-8. The vehicle remains near ground altitude, so the payload model is not yet ready to present as a completed slung-payload circuit.

![Payload failed altitude tracking](reports/payload_fig8_light_2026-06-05/payload_xyz_vs_time.png)

### 4. Payload Hover Validation

To isolate the problem, a hover-only controller was created and tested.

Payload hover test:

- Target: `x=0`, `y=0`, `z=-5 m` NED
- PX4 accepted arming/offboard and reported takeoff.
- Actual NED `z` stayed near ground level: `-0.083 m` to `0.050 m`.
- Mean hover tracking error: `4.997 m`.

Artifacts:

- Payload hover report: [`reports/payload_hover_2026-06-05/HOVER_VALIDATION_REPORT.md`](reports/payload_hover_2026-06-05/HOVER_VALIDATION_REPORT.md)
- XYZ-time plot: [`reports/payload_hover_2026-06-05/hover_xyz_vs_time.png`](reports/payload_hover_2026-06-05/hover_xyz_vs_time.png)
- Error plot: [`reports/payload_hover_2026-06-05/hover_tracking_error.png`](reports/payload_hover_2026-06-05/hover_tracking_error.png)

![Payload hover validation](reports/payload_hover_2026-06-05/hover_xyz_vs_time.png)

### 5. No-Payload Hover Control Check

The exact same `hover_offboard` node was run on the known-good `iris_depth_camera` model.

Result:

- Final NED `z`: `-5.010 m`
- Post-12s mean error: `0.067 m`
- Conclusion: ROS 2 offboard control is valid. The failure is isolated to the payload SDF/joint physics.

Artifacts:

- Control report: [`reports/hover_control_check_2026-06-05/HOVER_CONTROL_CHECK.md`](reports/hover_control_check_2026-06-05/HOVER_CONTROL_CHECK.md)
- Z plot: [`reports/hover_control_check_2026-06-05/hover_control_check_z.png`](reports/hover_control_check_2026-06-05/hover_control_check_z.png)

![No-payload hover control check](reports/hover_control_check_2026-06-05/hover_control_check_z.png)

## Installation

### 1. PX4 Autopilot

```bash
cd ~
git clone https://github.com/PX4/PX4-Autopilot.git --recursive
cd PX4-Autopilot
bash ./Tools/setup/ubuntu.sh
make px4_sitl_default -j2
```

### 2. ROS 2 Workspace

```bash
mkdir -p ~/ros2_ws/src
cp -r ./ros2_ws/src/uav_control ~/ros2_ws/src/
cd ~/ros2_ws
source /opt/ros/humble/setup.zsh
colcon build --packages-select uav_control
source install/setup.zsh
```

### 3. Micro XRCE-DDS Agent

```bash
MicroXRCEAgent udp4 -p 8888
```

If the command is missing, install/build the agent from eProsima's Micro-XRCE-DDS-Agent repository.

## Applying the PX4 Payload Integration Files

This repository stores the payload integration files under `px4_payload_integration/` using the same relative paths as PX4.

From the repository root:

```bash
PX4_DIR=~/PX4-Autopilot
cp px4_payload_integration/ROMFS/px4fmu_common/init.d-posix/airframes/1020_gazebo-classic_iris_depth_payload \
  "$PX4_DIR/ROMFS/px4fmu_common/init.d-posix/airframes/"

cp px4_payload_integration/ROMFS/px4fmu_common/init.d-posix/airframes/CMakeLists.txt \
  "$PX4_DIR/ROMFS/px4fmu_common/init.d-posix/airframes/CMakeLists.txt"

cp px4_payload_integration/src/modules/simulation/simulator_mavlink/sitl_targets_gazebo-classic.cmake \
  "$PX4_DIR/src/modules/simulation/simulator_mavlink/sitl_targets_gazebo-classic.cmake"

mkdir -p "$PX4_DIR/Tools/simulation/gazebo-classic/sitl_gazebo-classic/models/iris_depth_payload"
cp px4_payload_integration/Tools/simulation/gazebo-classic/sitl_gazebo-classic/models/iris_depth_payload/* \
  "$PX4_DIR/Tools/simulation/gazebo-classic/sitl_gazebo-classic/models/iris_depth_payload/"

cd "$PX4_DIR"
make px4_sitl_default -j2
```

## Run Commands

Use separate terminals.

### Terminal 1: MicroXRCEAgent

```bash
MicroXRCEAgent udp4 -p 8888
```

### Terminal 2: Baseline Depth-Camera SITL

```bash
cd ~/PX4-Autopilot
HEADLESS=1 make px4_sitl gazebo-classic_iris_depth_camera
```

### Terminal 3: Figure-8 Experiment

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.zsh
source install/setup.zsh
ros2 launch uav_control figure8_experiment.launch.py \
  metrics_path:=~/PX4-Autopilot/reports/figure8_tracking_metrics.csv \
  omega:=0.25
```

### Terminal 3 Alternative: Hover Validation

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.zsh
source install/setup.zsh
ros2 launch uav_control payload_hover_experiment.launch.py \
  metrics_path:=~/PX4-Autopilot/reports/payload_hover_tracking_metrics.csv \
  payload_metrics_path:=~/PX4-Autopilot/reports/payload_swing_metrics.csv \
  altitude_ned:=-5.0
```

### Payload SITL Target

After applying `px4_payload_integration/` to PX4:

```bash
cd ~/PX4-Autopilot
HEADLESS=1 make px4_sitl gazebo-classic_iris_depth_payload
```

## Known Limitations

The current payload model is intentionally documented as a work in progress.

- The payload airframe boots and arms.
- The payload logger receives Gazebo pose sniffer packets.
- The hover controller works on the no-payload model.
- The payload model does not climb under the same hover controller.

Most likely root cause: the current payload SDF/joint setup is interfering with Gazebo vehicle dynamics or link-frame constraints.

## Next Engineering Step

Do not continue payload figure-8 tuning until hover passes.

Recommended next sequence:

1. Create a minimal payload model with a fixed payload mass only.
2. Confirm it climbs to `z=-5 m` using `hover_offboard`.
3. Replace the fixed payload with a simple revolute/universal pendulum.
4. Validate Gazebo link poses for `iris::base_link`, `payload_cable`, and `slung_payload`.
5. Rerun payload hover.
6. Only then rerun payload figure-8.

## Notes for Professor-Facing Updates

Safe statement:

> The baseline ROS 2/PX4 offboard figure-8 circuit is complete and quantitatively logged. I have also added the first slung-payload SITL model and payload swing logger. The payload model currently boots and accepts offboard commands, but hover validation shows that the current cable/joint physics still prevents proper climb. I isolated this by running the same hover controller on the no-payload model, which successfully reaches the commanded altitude. The next task is therefore to correct the payload SDF joint model before presenting a completed slung-payload figure-8.

