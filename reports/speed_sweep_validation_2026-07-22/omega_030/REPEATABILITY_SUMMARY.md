# Controlled Repeatability Validation - 2026-07-22

## Purpose

This phase extends the clean June 12 restart from one controlled run per controller to a controlled repeatability set with the same launch, telemetry, and validation gates for every trial.

## Setup

- Vehicle: `iris_depth_payload`
- Payload: native ball-joint slung payload
- Trajectory: Figure-8
- Angular rate: `0.3 rad/s`
- Geometric hover thrust: `0.72`
- Trials: `3` PX4 baseline + `3` tuned geometric
- Validation gate: PX4 local position must remain within `100 m`
- Altitude gate: steady mean altitude must remain within `1.0 m` of `-5.0 m` NED
- Payload measurement: calibrated Gazebo same-frame link pair
- Raw per-trial telemetry CSV retention: `False`

## Trial Results

| profile | trial | tracking_valid | mean_3d_error_m | rms_3d_error_m | mean_z_ned_m | mean_lateral_swing_m | mean_cable_angle_deg |
| --- | --- | --- | --- | --- | --- | --- | --- |
| baseline | 1 | True | 0.6716 | 0.7158 | -4.9972 | 0.6575 | 41.4561 |
| baseline | 2 | True | 0.6791 | 0.7223 | -4.9965 | 0.6566 | 41.3939 |
| baseline | 3 | True | 0.6772 | 0.7201 | -4.9971 | 0.6564 | 41.3792 |
| geometric | 1 | True | 0.3842 | 0.4008 | -4.9978 | 0.5849 | 36.0347 |
| geometric | 2 | True | 0.3833 | 0.3999 | -4.9983 | 0.5854 | 36.0724 |
| geometric | 3 | True | 0.3849 | 0.4013 | -4.9983 | 0.5857 | 36.0965 |

## Aggregate Metrics

| profile | metric | mean | std | min | max |
| --- | --- | --- | --- | --- | --- |
| baseline | mean_3d_error_m | 0.6760 | 0.0039 | 0.6716 | 0.6791 |
| baseline | rms_3d_error_m | 0.7194 | 0.0033 | 0.7158 | 0.7223 |
| baseline | max_3d_error_m | 1.0372 | 0.0131 | 1.0250 | 1.0510 |
| baseline | mean_xy_error_m | 0.6758 | 0.0040 | 0.6713 | 0.6789 |
| baseline | mean_z_ned_m | -4.9969 | 0.0004 | -4.9972 | -4.9965 |
| baseline | mean_cable_length_m | 1.0016 | 0.0000 | 1.0016 | 1.0016 |
| baseline | mean_lateral_swing_m | 0.6569 | 0.0006 | 0.6564 | 0.6575 |
| baseline | max_lateral_swing_m | 0.8051 | 0.0009 | 0.8042 | 0.8060 |
| baseline | mean_cable_angle_deg | 41.4097 | 0.0409 | 41.3792 | 41.4561 |
| baseline | max_cable_angle_deg | 53.4291 | 0.0855 | 53.3418 | 53.5126 |
| geometric | mean_3d_error_m | 0.3841 | 0.0008 | 0.3833 | 0.3849 |
| geometric | rms_3d_error_m | 0.4006 | 0.0007 | 0.3999 | 0.4013 |
| geometric | max_3d_error_m | 0.6448 | 0.0082 | 0.6354 | 0.6504 |
| geometric | mean_xy_error_m | 0.3840 | 0.0008 | 0.3831 | 0.3847 |
| geometric | mean_z_ned_m | -4.9981 | 0.0003 | -4.9983 | -4.9978 |
| geometric | mean_cable_length_m | 1.0013 | 0.0000 | 1.0013 | 1.0013 |
| geometric | mean_lateral_swing_m | 0.5853 | 0.0004 | 0.5849 | 0.5857 |
| geometric | max_lateral_swing_m | 0.7448 | 0.0005 | 0.7444 | 0.7454 |
| geometric | mean_cable_angle_deg | 36.0678 | 0.0311 | 36.0347 | 36.0965 |
| geometric | max_cable_angle_deg | 48.0067 | 0.0425 | 47.9759 | 48.0551 |

## Controller Improvement

| metric | baseline_mean | geometric_mean | improvement_percent |
| --- | --- | --- | --- |
| mean_3d_error_m | 0.6760 | 0.3841 | 43.1727 |
| rms_3d_error_m | 0.7194 | 0.4006 | 44.3094 |
| mean_lateral_swing_m | 0.6569 | 0.5853 | 10.8903 |
| mean_cable_angle_deg | 41.4097 | 36.0678 | 12.9001 |

## Interpretation

All `6` trials completed with valid tracking and payload swing telemetry. The tuned geometric controller remains better than the PX4 position/velocity baseline over the small repeatability set, with lower mean tracking error and lower payload swing-angle metrics.

## Next Phase

Use this dataset to decide whether the controller comparison is stable enough to proceed to speed sweeps and payload-parameter sweeps.
