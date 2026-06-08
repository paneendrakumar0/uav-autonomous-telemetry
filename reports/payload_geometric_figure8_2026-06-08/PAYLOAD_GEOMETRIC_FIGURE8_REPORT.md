# Payload Geometric Figure-8 Validation - 2026-06-08

## Objective

Validate the tuned geometric attitude/thrust controller on the native ball-joint slung-payload model and compare it against the earlier PX4 position/velocity payload Figure-8 baseline.

## Setup

- Vehicle: `iris_depth_payload`
- Payload: native internal `base_link -> slung_payload` ball joint
- Controller: `geometric_figure8_attitude`
- Attitude topic: `/fmu/in/vehicle_attitude_setpoint_v1`
- Figure-8 amplitude: `5.0 m`
- Angular rate: `0.20 rad/s`
- Target altitude: `-5.0 m` NED
- Hover thrust parameter: `0.70`
- Steady-state analysis window: `t >= 20 s`

## Result

The slung-payload vehicle completed the geometric-controller Figure-8 run. PX4 accepted fresh attitude/thrust setpoints, detected takeoff, held altitude near the target, and landed/disarmed after the timed run.

## Tracking Metrics

- Samples: `4731`
- Duration: `94.62 s`
- Post-20s mean 3D error: `0.315 m`
- Post-20s RMS 3D error: `0.322 m`
- Post-20s maximum 3D error: `0.482 m`
- Post-20s mean XY error: `0.281 m`
- Post-20s mean altitude: `-4.864 m` NED
- Final altitude: `-4.867 m` NED
- Actual X range: `-4.981 m` to `4.907 m`
- Actual Y range: `-2.465 m` to `2.535 m`

## Baseline Comparison

| Controller | Payload | Steady Window | Mean 3D Error | RMS 3D Error | Max 3D Error | Mean Z NED |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| PX4 position/velocity | yes | `t >= 25 s` | `0.462 m` | `0.493 m` | `0.796 m` | `-4.996 m` |
| Geometric attitude/thrust | yes | `t >= 20 s` | `0.315 m` | `0.322 m` | `0.482 m` | `-4.864 m` |

The geometric attitude/thrust controller improves the payload Figure-8 tracking error in this run while using a slightly slower angular rate (`0.20 rad/s`) than the earlier payload baseline (`0.25 rad/s`). The next fair comparison should repeat both controllers at matched angular rates.

## Payload Swing Diagnostics

- Payload samples: `23593`
- Post-20s mean lateral swing: `5.091 m`
- Post-20s maximum lateral swing: `9.351 m`
- Post-20s mean cable angle: `75.867 deg`
- Post-20s maximum cable angle: `85.025 deg`
- Post-20s mean cable length estimate: `5.189 m`

As in earlier runs, the swing values are diagnostic because the pose-sniffer frame convention still needs calibration before physical cable-angle claims.

## Artifacts

- `geometric_payload_figure8_tracking_metrics.csv`
- `geometric_payload_swing_metrics.csv`
- `payload_geometric_xy_tracking.png`
- `payload_geometric_xy_tracking_steady.png`
- `payload_geometric_3d_tracking.png`
- `payload_geometric_xyz_error.png`
- `payload_geometric_swing_diagnostics.png`
