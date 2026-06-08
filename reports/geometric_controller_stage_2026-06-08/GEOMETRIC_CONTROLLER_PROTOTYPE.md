# Geometric Controller Prototype - 2026-06-08

## Objective

Start the controller-upgrade stage requested after the successful slung-payload Figure-8 baseline. The current validated controller uses PX4 offboard position/velocity setpoints. This stage adds a separate attitude/thrust prototype so future runs can compare:

- PX4 position/velocity baseline
- Geometric attitude/thrust control
- Later payload-aware swing-reduction variants

## Added Node

New executable:

```text
geometric_figure8_attitude
```

Source:

```text
ros2_ws/src/uav_control/src/geometric_figure8_attitude.cpp
```

The node:

- subscribes to `/fmu/out/vehicle_local_position_v1`
- publishes `/fmu/in/offboard_control_mode` with attitude mode enabled
- publishes `/fmu/in/vehicle_attitude_setpoint`
- publishes `/fmu/in/vehicle_command` for offboard/arming
- also publishes `/fmu/in/trajectory_setpoint` as a reference stream for the existing metrics logger

The reference stream preserves the same CSV/plot pipeline used for the validated Figure-8 runs.

## Controller Form

The prototype computes a desired acceleration from position and velocity error:

```text
a_cmd = a_ref - Kp * (x - x_ref) - Kd * (v - v_ref)
```

It then converts the commanded acceleration into:

- desired body-z direction
- attitude quaternion
- normalized thrust command

This is intentionally kept as a separate prototype rather than replacing the validated `figure8_offboard` baseline.

## Launch File

New launch file:

```text
ros2_ws/src/uav_control/launch/geometric_figure8_experiment.launch.py
```

Example command:

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.zsh
source install/setup.zsh
ros2 launch uav_control geometric_figure8_experiment.launch.py \
  metrics_path:=~/PX4-Autopilot/reports/geometric_figure8_tracking_metrics.csv \
  payload_metrics_path:=~/PX4-Autopilot/reports/geometric_payload_swing_metrics.csv \
  amplitude:=5.0 \
  omega:=0.20 \
  altitude_ned:=-5.0 \
  hover_thrust:=0.62
```

## Commissioning Plan

Recommended validation sequence:

1. Run no-payload hover/slow Figure-8 first with the attitude controller.
2. Tune `hover_thrust`, `kp_xy`, `kp_z`, `kd_xy`, and `kd_z` until altitude is stable.
3. Repeat the no-payload Figure-8 benchmark.
4. Run the native ball-joint payload hover.
5. Run the native ball-joint payload Figure-8 only after the no-payload case is stable.

## Current Status

- Code added.
- Launch file added.
- Build validation completed with `colcon build --packages-select uav_control`.
- Flight validation is intentionally still pending; the proven PX4 position/velocity controller remains the current research baseline until this prototype is tuned in SITL.
