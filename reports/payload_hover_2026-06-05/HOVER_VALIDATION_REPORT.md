# Payload Hover Validation - 2026-06-05

## Result

The hover-only offboard stage was implemented and executed. PX4 accepted the external arm/offboard command and reported takeoff detected, but the payload vehicle did not climb toward the commanded hover altitude.

## Run Configuration

- SITL target: `gazebo-classic_iris_depth_payload`
- Hover target: `x=0 m`, `y=0 m`, `z=-5 m` NED
- Payload model: lightweight baseline payload, 0.05 kg payload mass, near-zero cable mass
- ROS 2 launch: `payload_hover_experiment.launch.py`

## Metrics

Trajectory CSV: `hover_tracking_metrics.csv`

- Samples: 3831
- Duration: 76.61 s
- Mean tracking error: 4.997 m
- RMS tracking error: 4.997 m
- Max tracking error: 5.050 m
- Post-12s mean tracking error: 4.998 m
- Actual NED z range: -0.083 to 0.050 m
- Mean vertical velocity: -0.0011 m/s

Payload CSV: `payload_swing_metrics.csv`

- Samples: 19109
- Post-12s mean cable angle estimate: 83.057 deg
- Post-12s max lateral offset estimate: 1.280 m

## Interpretation

The hover controller and logging pipeline are working. The failure is below the guidance layer: the vehicle remains near ground level despite an accepted offboard hover setpoint. This strongly suggests the current payload SDF/joint setup is still interfering with the Gazebo vehicle dynamics or frame linkage.

## Next Fix Target

Do not continue to payload Figure-8 until hover passes. The next coding/debug pass should isolate the SDF physics:

1. Run the same hover controller on `iris_depth_camera` to confirm the new hover node climbs normally without payload.
2. Create a minimal payload model variant using a fixed payload first, then replace it with a pendulum joint after lift is confirmed.
3. Validate Gazebo link poses for `iris::base_link`, `payload_cable`, and `slung_payload` before arming.
4. Only after `actual_z` reaches approximately `-5 m`, rerun payload Figure-8.

## Generated Plots

- `hover_xyz_vs_time.png`
- `hover_tracking_error.png`
- `hover_xy_drift.png`
- `payload_hover_3d.png`
- `hover_payload_cable_angle.png`

## Plot Preview

![Payload hover XY drift](hover_xy_drift.png)

![Payload hover 3D trajectory](payload_hover_3d.png)

![Payload hover XYZ versus time](hover_xyz_vs_time.png)

## Control Check Added

A no-payload control run was executed with the same `hover_offboard` node on `gazebo-classic_iris_depth_camera`.

Result: the vehicle climbed normally to `z=-5 m` NED and ended near `z=-4.993 m`. This confirms the hover/offboard controller is working, and the payload hover failure is isolated to the `iris_depth_payload` Gazebo model/joint physics.

Control-check report: `../hover_control_check_2026-06-05/HOVER_CONTROL_CHECK.md`
