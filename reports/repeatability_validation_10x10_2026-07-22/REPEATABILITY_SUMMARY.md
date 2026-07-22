# Controlled Repeatability Validation - 2026-07-22

## Purpose

This phase extends the clean June 12 restart from one controlled run per controller to a controlled repeatability set with the same launch, telemetry, and validation gates for every trial.

## Setup

- Vehicle: `iris_depth_payload`
- Payload: native ball-joint slung payload
- Trajectory: Figure-8
- Angular rate: `0.25 rad/s`
- Geometric hover thrust: `0.72`
- Trials: `10` PX4 baseline + `10` tuned geometric
- Validation gate: PX4 local position must remain within `100 m`
- Altitude gate: steady mean altitude must remain within `1.0 m` of `-5.0 m` NED
- Payload measurement: calibrated Gazebo same-frame link pair
- Raw per-trial telemetry CSV retention: `False`

## Trial Results

| profile | trial | tracking_valid | mean_3d_error_m | rms_3d_error_m | mean_z_ned_m | mean_lateral_swing_m | mean_cable_angle_deg |
| --- | --- | --- | --- | --- | --- | --- | --- |
| baseline | 1 | True | 0.4451 | 0.4751 | -4.9988 | 0.5622 | 34.4427 |
| baseline | 2 | True | 0.4429 | 0.4731 | -4.9987 | 0.5638 | 34.5612 |
| baseline | 3 | True | 0.4450 | 0.4752 | -4.9993 | 0.5648 | 34.6269 |
| baseline | 4 | True | 0.4474 | 0.4771 | -4.9988 | 0.5644 | 34.5987 |
| baseline | 5 | True | 0.4450 | 0.4755 | -4.9990 | 0.5645 | 34.6077 |
| baseline | 6 | True | 0.4460 | 0.4760 | -4.9984 | 0.5637 | 34.5531 |
| baseline | 7 | True | 0.4458 | 0.4763 | -4.9989 | 0.5645 | 34.6058 |
| baseline | 8 | True | 0.4431 | 0.4740 | -4.9990 | 0.5640 | 34.5718 |
| baseline | 9 | True | 0.4457 | 0.4754 | -4.9983 | 0.5637 | 34.5504 |
| baseline | 10 | True | 0.4453 | 0.4760 | -4.9988 | 0.5646 | 34.6136 |
| geometric | 1 | True | 0.3360 | 0.3519 | -4.9942 | 0.5145 | 31.1405 |
| geometric | 2 | True | 0.3379 | 0.3533 | -4.9948 | 0.5141 | 31.1151 |
| geometric | 3 | True | 0.3377 | 0.3533 | -4.9948 | 0.5147 | 31.1523 |
| geometric | 4 | True | 0.3271 | 0.3519 | -4.9944 | 0.5138 | 31.0929 |
| geometric | 5 | True | 0.3811 | 0.4188 | -4.9945 | 0.5079 | 30.7317 |
| geometric | 6 | True | 0.3367 | 0.3523 | -4.9947 | 0.5144 | 31.1401 |
| geometric | 7 | True | 0.3389 | 0.3545 | -4.9947 | 0.5147 | 31.1516 |
| geometric | 8 | True | 0.3362 | 0.3522 | -4.9948 | 0.5146 | 31.1471 |
| geometric | 9 | True | 0.3291 | 0.3526 | -4.9938 | 0.5131 | 31.0517 |
| geometric | 10 | True | 0.3363 | 0.3510 | -4.9951 | 0.5145 | 31.1410 |

## Aggregate Metrics

| profile | metric | mean | std | min | max |
| --- | --- | --- | --- | --- | --- |
| baseline | mean_3d_error_m | 0.4451 | 0.0013 | 0.4429 | 0.4474 |
| baseline | rms_3d_error_m | 0.4754 | 0.0012 | 0.4731 | 0.4771 |
| baseline | max_3d_error_m | 0.6717 | 0.0048 | 0.6609 | 0.6764 |
| baseline | mean_xy_error_m | 0.4448 | 0.0013 | 0.4425 | 0.4470 |
| baseline | mean_z_ned_m | -4.9988 | 0.0003 | -4.9993 | -4.9983 |
| baseline | mean_cable_length_m | 1.0012 | 0.0000 | 1.0012 | 1.0012 |
| baseline | mean_lateral_swing_m | 0.5640 | 0.0008 | 0.5622 | 0.5648 |
| baseline | max_lateral_swing_m | 0.7311 | 0.0006 | 0.7301 | 0.7318 |
| baseline | mean_cable_angle_deg | 34.5732 | 0.0532 | 34.4427 | 34.6269 |
| baseline | max_cable_angle_deg | 46.8502 | 0.0498 | 46.7727 | 46.9139 |
| geometric | mean_3d_error_m | 0.3397 | 0.0150 | 0.3271 | 0.3811 |
| geometric | rms_3d_error_m | 0.3592 | 0.0210 | 0.3510 | 0.4188 |
| geometric | max_3d_error_m | 0.5976 | 0.0576 | 0.5529 | 0.7564 |
| geometric | mean_xy_error_m | 0.3394 | 0.0150 | 0.3267 | 0.3807 |
| geometric | mean_z_ned_m | -4.9946 | 0.0004 | -4.9951 | -4.9938 |
| geometric | mean_cable_length_m | 1.0010 | 0.0000 | 1.0010 | 1.0010 |
| geometric | mean_lateral_swing_m | 0.5136 | 0.0021 | 0.5079 | 0.5147 |
| geometric | max_lateral_swing_m | 0.6746 | 0.0019 | 0.6707 | 0.6785 |
| geometric | mean_cable_angle_deg | 31.0864 | 0.1287 | 30.7317 | 31.1523 |
| geometric | max_cable_angle_deg | 42.3288 | 0.1440 | 42.0330 | 42.6294 |

## Controller Improvement

| metric | baseline_mean | geometric_mean | improvement_percent |
| --- | --- | --- | --- |
| mean_3d_error_m | 0.4451 | 0.3397 | 23.6834 |
| rms_3d_error_m | 0.4754 | 0.3592 | 24.4419 |
| mean_lateral_swing_m | 0.5640 | 0.5136 | 8.9335 |
| mean_cable_angle_deg | 34.5732 | 31.0864 | 10.0853 |

## Interpretation

All `20` trials completed with valid tracking and payload swing telemetry. The tuned geometric controller remains better than the PX4 position/velocity baseline over the `10 + 10` repeatability set, with lower mean tracking error and lower payload swing-angle metrics.

The geometric set includes one valid tracking-error outlier in trial `5` (`0.3811 m` mean 3D error, `0.4188 m` RMS error). This outlier was retained because it passed all validation gates and had valid payload telemetry. Even with that outlier included, the geometric controller improves mean 3D tracking error by `23.68%`, RMS tracking error by `24.44%`, mean lateral swing by `8.93%`, and mean cable angle by `10.09%`.

## Next Phase

Use this dataset to decide whether the controller comparison is stable enough to proceed to speed sweeps and payload-parameter sweeps.
