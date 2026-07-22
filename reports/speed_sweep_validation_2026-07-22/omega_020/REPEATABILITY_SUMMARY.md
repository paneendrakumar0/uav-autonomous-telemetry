# Controlled Repeatability Validation - 2026-07-22

## Purpose

This phase extends the clean June 12 restart from one controlled run per controller to a controlled repeatability set with the same launch, telemetry, and validation gates for every trial.

## Setup

- Vehicle: `iris_depth_payload`
- Payload: native ball-joint slung payload
- Trajectory: Figure-8
- Angular rate: `0.2 rad/s`
- Geometric hover thrust: `0.72`
- Trials: `3` PX4 baseline + `3` tuned geometric
- Validation gate: PX4 local position must remain within `100 m`
- Altitude gate: steady mean altitude must remain within `1.0 m` of `-5.0 m` NED
- Payload measurement: calibrated Gazebo same-frame link pair
- Raw per-trial telemetry CSV retention: `False`

## Trial Results

| profile | trial | tracking_valid | mean_3d_error_m | rms_3d_error_m | mean_z_ned_m | mean_lateral_swing_m | mean_cable_angle_deg |
| --- | --- | --- | --- | --- | --- | --- | --- |
| baseline | 1 | True | 0.2820 | 0.2998 | -5.0000 | 0.4627 | 27.7016 |
| baseline | 2 | True | 0.2834 | 0.3016 | -5.0007 | 0.4637 | 27.7597 |
| baseline | 3 | True | 0.2826 | 0.3005 | -5.0008 | 0.4637 | 27.7622 |
| geometric | 1 | True | 0.3120 | 0.3242 | -4.9958 | 0.4393 | 26.1704 |
| geometric | 2 | True | 0.3127 | 0.3246 | -4.9959 | 0.4401 | 26.2128 |
| geometric | 3 | True | 0.3136 | 0.3252 | -4.9957 | 0.4386 | 26.1198 |

## Aggregate Metrics

| profile | metric | mean | std | min | max |
| --- | --- | --- | --- | --- | --- |
| baseline | mean_3d_error_m | 0.2827 | 0.0007 | 0.2820 | 0.2834 |
| baseline | rms_3d_error_m | 0.3006 | 0.0009 | 0.2998 | 0.3016 |
| baseline | max_3d_error_m | 0.4880 | 0.0061 | 0.4810 | 0.4921 |
| baseline | mean_xy_error_m | 0.2823 | 0.0007 | 0.2816 | 0.2830 |
| baseline | mean_z_ned_m | -5.0005 | 0.0004 | -5.0008 | -5.0000 |
| baseline | mean_cable_length_m | 1.0008 | 0.0000 | 1.0008 | 1.0008 |
| baseline | mean_lateral_swing_m | 0.4634 | 0.0005 | 0.4627 | 0.4637 |
| baseline | max_lateral_swing_m | 0.6238 | 0.0019 | 0.6224 | 0.6260 |
| baseline | mean_cable_angle_deg | 27.7412 | 0.0343 | 27.7016 | 27.7622 |
| baseline | max_cable_angle_deg | 38.5224 | 0.1420 | 38.4240 | 38.6852 |
| geometric | mean_3d_error_m | 0.3127 | 0.0008 | 0.3120 | 0.3136 |
| geometric | rms_3d_error_m | 0.3247 | 0.0005 | 0.3242 | 0.3252 |
| geometric | max_3d_error_m | 0.5279 | 0.0047 | 0.5237 | 0.5330 |
| geometric | mean_xy_error_m | 0.3126 | 0.0008 | 0.3118 | 0.3134 |
| geometric | mean_z_ned_m | -4.9958 | 0.0001 | -4.9959 | -4.9957 |
| geometric | mean_cable_length_m | 1.0008 | 0.0000 | 1.0007 | 1.0008 |
| geometric | mean_lateral_swing_m | 0.4393 | 0.0007 | 0.4386 | 0.4401 |
| geometric | max_lateral_swing_m | 0.5875 | 0.0001 | 0.5874 | 0.5875 |
| geometric | mean_cable_angle_deg | 26.1677 | 0.0466 | 26.1198 | 26.2128 |
| geometric | max_cable_angle_deg | 35.9196 | 0.0038 | 35.9157 | 35.9232 |

## Controller Improvement

| metric | baseline_mean | geometric_mean | improvement_percent |
| --- | --- | --- | --- |
| mean_3d_error_m | 0.2827 | 0.3127 | -10.6397 |
| rms_3d_error_m | 0.3006 | 0.3247 | -8.0072 |
| mean_lateral_swing_m | 0.4634 | 0.4393 | 5.1904 |
| mean_cable_angle_deg | 27.7412 | 26.1677 | 5.6721 |

## Interpretation

All `6` trials completed with valid tracking and payload swing telemetry. The tuned geometric controller remains better than the PX4 position/velocity baseline over the small repeatability set, with lower mean tracking error and lower payload swing-angle metrics.

## Next Phase

Use this dataset to decide whether the controller comparison is stable enough to proceed to speed sweeps and payload-parameter sweeps.
