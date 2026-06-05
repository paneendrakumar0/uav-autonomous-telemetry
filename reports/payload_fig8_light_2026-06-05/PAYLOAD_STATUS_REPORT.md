# Slung Payload Figure-8 Baseline Attempt - 2026-06-05

## Result

The slung-payload Gazebo Classic model now starts, PX4 finds the new airframe (`SYS_AUTOSTART=1020`), MicroXRCEAgent connects, the ROS 2 figure-8 controller launches, and PX4 accepts external arming/offboard commands. However, the current payload model is not yet producing a valid airborne figure-8: the vehicle remains near ground altitude even after arming and takeoff detection.

## What was completed

- Added Gazebo Classic model `iris_depth_payload` with depth camera, cable link, and slung payload link.
- Added PX4 airframe `1020_gazebo-classic_iris_depth_payload` and registered it in the ROMFS airframe list.
- Registered the model target in the Gazebo Classic SITL target list.
- Added ROS 2 payload experiment launch file and payload swing logger.
- Built PX4 SITL and ROS 2 `uav_control` successfully.
- Ran multiple SITL attempts and captured CSV evidence.

## Current Run Metrics

Trajectory CSV: `figure8_tracking_metrics.csv`

- Samples: 6589
- Duration: 131.78 s
- Full-run mean tracking error: 6.335 m
- Full-run RMS tracking error: 6.379 m
- Full-run max tracking error: 7.141 m
- Post-12s mean tracking error: 6.329 m
- Actual NED z range: -0.083 to 0.054 m

Payload CSV: `payload_swing_metrics.csv`

- Samples: 32900
- Full-run mean cable angle estimate: 82.960 deg
- Post-12s mean cable angle estimate: 82.926 deg
- Post-12s max lateral offset estimate: 1.311 m

## Interpretation

The model/airframe integration stage is partially complete: it boots, publishes sensor topics, accepts offboard commands, and logs payload pose packets. The remaining blocker is physical/model-frame correctness in the payload joint setup. The vehicle arms, but the local-position trace stays around ground level instead of converging to the commanded `z=-5 m`, so the current payload SDF should not be presented as a completed 8-shape payload circuit yet.

Most likely next fixes:

1. Rework the payload joint anchor so the cable does not constrain the nested `iris::base_link` incorrectly.
2. Validate link poses through Gazebo ground-truth/model-state topics before running offboard.
3. Start with a hover-only payload test, then run the 8-shape after altitude tracking is confirmed.
4. Increase payload mass gradually only after hover and altitude tracking are stable.

## Generated Plots

- `payload_xy_tracking.png`
- `payload_xyz_vs_time.png`
- `payload_tracking_error.png`
- `payload_cable_angle.png`
- `payload_lateral_swing.png`
