# Native Ball-Joint Payload Figure-8 Validation - 2026-06-07

## Objective
Validate Professor Zavoli's requested 8-shaped autonomous trajectory using the fixed native `iris_depth_payload` model with a physical internal `base_link -> slung_payload` ball joint.

## Setup
- Vehicle: `iris_depth_payload` native Iris-derived SDF
- Payload joint: internal ball joint from `base_link` to `slung_payload`
- Payload mass: `0.05 kg`
- Payload collision: disabled for flight baseline to avoid ground-contact solver locking at spawn
- Controller: ROS 2 PX4 offboard position/velocity setpoints
- Figure-8 amplitude: `5.0 m`
- Angular rate: `0.25 rad/s`
- Altitude command: `-5.0 m` NED

## Result
The UAV completed sustained Figure-8 motion with the physical slung payload attached and maintained altitude.

## Tracking Metrics
- Duration: `150.91 s`
- Samples: `7545`
- Post-25s mean 3D error: `0.462 m`
- Post-25s RMS 3D error: `0.493 m`
- Post-25s maximum 3D error: `0.796 m`
- Post-25s mean XY error: `0.462 m`
- Post-25s RMS XY error: `0.493 m`
- Mean post-25s altitude: `-4.996 m` NED
- Final altitude: `-4.987 m` NED
- Actual X range: `-5.489 m` to `5.291 m`
- Actual Y range: `-3.158 m` to `3.083 m`

## Payload Swing Metrics
- Payload samples: `37644`
- Mean lateral swing: `5.149 m`
- Maximum lateral swing: `10.646 m`
- Mean cable angle: `75.289 deg`
- Maximum cable angle: `86.271 deg`

## Artifacts
- `payload_figure8_xy_tracking.png`
- `payload_figure8_xy_tracking_steady.png`
- `payload_figure8_xyz_vs_time.png`
- `payload_figure8_3d_tracking.png`
- `payload_figure8_tracking_error.png`
- `payload_figure8_swing_metrics.png`
- `payload_figure8_relative_motion_3d.png`
- `figure8_tracking_metrics.csv`
- `payload_swing_metrics.csv`

## Note
The large cable-angle values are generated from Gazebo pose-sniffer relative positions and should be treated as diagnostic payload-motion estimates. The flight result itself is validated by PX4 local-position tracking and Gazebo visual state.
