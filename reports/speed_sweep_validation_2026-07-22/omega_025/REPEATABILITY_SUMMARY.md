# Controlled Repeatability Validation - 2026-07-22

## Purpose

This phase extends the clean June 12 restart from one controlled run per controller to a controlled repeatability set with the same launch, telemetry, and validation gates for every trial.

## Setup

- Vehicle: `iris_depth_payload`
- Payload: native ball-joint slung payload
- Trajectory: Figure-8
- Angular rate: `0.25 rad/s`
- Geometric hover thrust: `0.72`
- Trials: `3` PX4 baseline + `3` tuned geometric
- Validation gate: PX4 local position must remain within `100 m`
- Altitude gate: steady mean altitude must remain within `1.0 m` of `-5.0 m` NED
- Payload measurement: calibrated Gazebo same-frame link pair
- Raw per-trial telemetry CSV retention: `False`

## Trial Results

| profile | trial | tracking_valid | mean_3d_error_m | rms_3d_error_m | mean_z_ned_m | mean_lateral_swing_m | mean_cable_angle_deg |
| --- | --- | --- | --- | --- | --- | --- | --- |
| baseline | 1 | True | 0.4465 | 0.4765 | -4.9989 | 0.5642 | 34.5868 |
| baseline | 2 | True | 0.4458 | 0.4755 | -4.9984 | 0.5639 | 34.5675 |
| baseline | 3 | True | 0.4453 | 0.4757 | -4.9990 | 0.5644 | 34.5977 |
| geometric | 1 | True | 0.3395 | 0.3549 | -4.9947 | 0.5145 | 31.1408 |
| geometric | 2 | True | 0.3393 | 0.3549 | -4.9949 | 0.5146 | 31.1444 |
| geometric | 3 | True | 0.3372 | 0.3529 | -4.9944 | 0.5150 | 31.1707 |

## Aggregate Metrics

| profile | metric | mean | std | min | max |
| --- | --- | --- | --- | --- | --- |
| baseline | mean_3d_error_m | 0.4459 | 0.0006 | 0.4453 | 0.4465 |
| baseline | rms_3d_error_m | 0.4759 | 0.0005 | 0.4755 | 0.4765 |
| baseline | max_3d_error_m | 0.6755 | 0.0032 | 0.6724 | 0.6788 |
| baseline | mean_xy_error_m | 0.4455 | 0.0006 | 0.4450 | 0.4461 |
| baseline | mean_z_ned_m | -4.9988 | 0.0003 | -4.9990 | -4.9984 |
| baseline | mean_cable_length_m | 1.0012 | 0.0000 | 1.0012 | 1.0012 |
| baseline | mean_lateral_swing_m | 0.5642 | 0.0003 | 0.5639 | 0.5644 |
| baseline | max_lateral_swing_m | 0.7313 | 0.0008 | 0.7308 | 0.7322 |
| baseline | mean_cable_angle_deg | 34.5840 | 0.0153 | 34.5675 | 34.5977 |
| baseline | max_cable_angle_deg | 46.8667 | 0.0648 | 46.8243 | 46.9413 |
| geometric | mean_3d_error_m | 0.3387 | 0.0013 | 0.3372 | 0.3395 |
| geometric | rms_3d_error_m | 0.3543 | 0.0012 | 0.3529 | 0.3549 |
| geometric | max_3d_error_m | 0.5868 | 0.0087 | 0.5810 | 0.5969 |
| geometric | mean_xy_error_m | 0.3384 | 0.0013 | 0.3369 | 0.3393 |
| geometric | mean_z_ned_m | -4.9947 | 0.0002 | -4.9949 | -4.9944 |
| geometric | mean_cable_length_m | 1.0010 | 0.0000 | 1.0010 | 1.0010 |
| geometric | mean_lateral_swing_m | 0.5147 | 0.0002 | 0.5145 | 0.5150 |
| geometric | max_lateral_swing_m | 0.6755 | 0.0010 | 0.6743 | 0.6763 |
| geometric | mean_cable_angle_deg | 31.1520 | 0.0163 | 31.1408 | 31.1707 |
| geometric | max_cable_angle_deg | 42.3985 | 0.0803 | 42.3095 | 42.4654 |

## Controller Improvement

| metric | baseline_mean | geometric_mean | improvement_percent |
| --- | --- | --- | --- |
| mean_3d_error_m | 0.4459 | 0.3387 | 24.0418 |
| rms_3d_error_m | 0.4759 | 0.3543 | 25.5636 |
| mean_lateral_swing_m | 0.5642 | 0.5147 | 8.7694 |
| mean_cable_angle_deg | 34.5840 | 31.1520 | 9.9238 |

## Interpretation

All `6` trials completed with valid tracking and payload swing telemetry. The tuned geometric controller remains better than the PX4 position/velocity baseline over the small repeatability set, with lower mean tracking error and lower payload swing-angle metrics.

## Next Phase

Use this dataset to decide whether the controller comparison is stable enough to proceed to speed sweeps and payload-parameter sweeps.
