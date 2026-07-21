# Controlled Baseline vs Geometric Validation - 2026-07-21

## Purpose

This phase restarts the project from the stable June 12 state and validates both controllers using the same controlled launch procedure. Each run explicitly starts `MicroXRCEAgent`, PX4 SITL, ROS 2 offboard control, tracking logging, and calibrated payload swing logging.

## Setup

- Vehicle: `iris_depth_payload`
- Payload: native `base_link -> slung_payload` ball joint
- Trajectory: Figure-8, amplitude `5.0 m`
- Angular rate: `0.25 rad/s`
- Target altitude: `-5.0 m` NED
- Geometric hover thrust: `0.72`
- Steady-state window: `t >= 25 s`
- Payload measurement: Gazebo same-frame link pair

## Results

| Metric | PX4 Position/Velocity Baseline | Tuned Geometric Controller |
| --- | ---: | ---: |
| Tracking valid | `true` | `true` |
| Samples | `3708` | `3721` |
| Duration | `74.148 s` | `74.404 s` |
| Mean 3D tracking error | `0.441 m` | `0.321 m` |
| RMS 3D tracking error | `0.472 m` | `0.335 m` |
| Max 3D tracking error | `0.667 m` | `0.556 m` |
| Mean XY tracking error | `0.441 m` | `0.320 m` |
| Mean altitude | `-4.999 m` NED | `-4.993 m` NED |
| Mean cable length | `1.001 m` | `1.001 m` |
| Mean lateral swing | `0.564 m` | `0.518 m` |
| Max lateral swing | `0.730 m` | `0.672 m` |
| Mean cable angle | `34.545 deg` | `31.333 deg` |
| Max cable angle | `46.772 deg` | `42.145 deg` |

## Improvements

- Mean 3D tracking error reduced by `27.3%`.
- RMS 3D tracking error reduced by `29.0%`.
- Mean lateral payload swing reduced by `8.1%`.
- Mean cable angle reduced by `9.3%`.

## Interpretation

The clean rerun confirms the June 12 conclusion: the tuned geometric attitude/thrust controller tracks the requested Figure-8 more accurately than the PX4 position/velocity baseline while also reducing the payload swing metrics. Both runs have sane PX4 local-position telemetry and calibrated same-frame payload measurements, so this comparison is suitable as the starting point for repeatability testing.

## Artifacts

Baseline:

- `../single_validation_2026-07-21_baseline_june12/VALIDATION_SUMMARY.md`
- `../single_validation_2026-07-21_baseline_june12/validation_xy_tracking.png`
- `../single_validation_2026-07-21_baseline_june12/validation_3d_tracking.png`
- `../single_validation_2026-07-21_baseline_june12/validation_xyz_vs_time.png`
- `../single_validation_2026-07-21_baseline_june12/validation_error_swing.png`

Geometric:

- `../single_validation_2026-07-21_geometric_june12_rerun/VALIDATION_SUMMARY.md`
- `../single_validation_2026-07-21_geometric_june12_rerun/validation_xy_tracking.png`
- `../single_validation_2026-07-21_geometric_june12_rerun/validation_3d_tracking.png`
- `../single_validation_2026-07-21_geometric_june12_rerun/validation_xyz_vs_time.png`
- `../single_validation_2026-07-21_geometric_june12_rerun/validation_error_swing.png`

## Next Phase

Run repeatability testing with a small clean sample first: three baseline runs and three tuned-geometric runs using the same controlled launcher. Scale to larger batches only after the six-run repeatability set remains telemetry-valid.
