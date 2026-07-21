# Controlled Repeatability Validation - 2026-07-21

## Purpose

This phase extends the clean June 12 restart from one controlled run per controller to a controlled repeatability set with the same launch, telemetry, and validation gates for every trial.

## Setup

- Vehicle: `iris_depth_payload`
- Payload: native ball-joint slung payload
- Trajectory: Figure-8
- Angular rate: `0.25 rad/s`
- Geometric hover thrust: `0.72`
- Trials: `5` PX4 baseline + `5` tuned geometric
- Validation gate: PX4 local position must remain within `100 m`
- Payload measurement: calibrated Gazebo same-frame link pair

## Trial Results

| profile | trial | tracking_valid | mean_3d_error_m | rms_3d_error_m | mean_z_ned_m | mean_lateral_swing_m | mean_cable_angle_deg |
| --- | --- | --- | --- | --- | --- | --- | --- |
| baseline | 1 | True | 0.4443 | 0.4742 | -4.9986 | 0.5636 | 34.5451 |
| baseline | 2 | True | 0.4457 | 0.4752 | -4.9988 | 0.5643 | 34.5967 |
| baseline | 3 | True | 0.4473 | 0.4771 | -4.9988 | 0.5645 | 34.6091 |
| baseline | 4 | True | 0.4453 | 0.4758 | -4.9990 | 0.5644 | 34.6003 |
| baseline | 5 | True | 0.4435 | 0.4738 | -4.9985 | 0.5637 | 34.5518 |
| geometric | 1 | True | 0.3374 | 0.3534 | -4.9947 | 0.5142 | 31.1179 |
| geometric | 2 | True | 0.3398 | 0.3549 | -4.9951 | 0.5141 | 31.1158 |
| geometric | 3 | True | 0.3812 | 0.4181 | -4.9937 | 0.5068 | 30.6596 |
| geometric | 4 | True | 0.3370 | 0.3511 | -4.9946 | 0.5141 | 31.1144 |
| geometric | 5 | True | 0.3375 | 0.3534 | -4.9948 | 0.5143 | 31.1274 |

## Aggregate Metrics

| profile | metric | mean | std | min | max |
| --- | --- | --- | --- | --- | --- |
| baseline | mean_3d_error_m | 0.4452 | 0.0015 | 0.4435 | 0.4473 |
| baseline | rms_3d_error_m | 0.4752 | 0.0013 | 0.4738 | 0.4771 |
| baseline | max_3d_error_m | 0.6718 | 0.0025 | 0.6690 | 0.6744 |
| baseline | mean_xy_error_m | 0.4449 | 0.0015 | 0.4431 | 0.4469 |
| baseline | mean_z_ned_m | -4.9987 | 0.0002 | -4.9990 | -4.9985 |
| baseline | mean_cable_length_m | 1.0012 | 0.0000 | 1.0012 | 1.0012 |
| baseline | mean_lateral_swing_m | 0.5641 | 0.0005 | 0.5636 | 0.5645 |
| baseline | max_lateral_swing_m | 0.7310 | 0.0006 | 0.7301 | 0.7315 |
| baseline | mean_cable_angle_deg | 34.5806 | 0.0298 | 34.5451 | 34.6091 |
| baseline | max_cable_angle_deg | 46.8441 | 0.0489 | 46.7690 | 46.8846 |
| geometric | mean_3d_error_m | 0.3466 | 0.0194 | 0.3370 | 0.3812 |
| geometric | rms_3d_error_m | 0.3662 | 0.0291 | 0.3511 | 0.4181 |
| geometric | max_3d_error_m | 0.6157 | 0.0720 | 0.5748 | 0.7437 |
| geometric | mean_xy_error_m | 0.3464 | 0.0193 | 0.3368 | 0.3809 |
| geometric | mean_z_ned_m | -4.9946 | 0.0005 | -4.9951 | -4.9937 |
| geometric | mean_cable_length_m | 1.0010 | 0.0000 | 1.0010 | 1.0010 |
| geometric | mean_lateral_swing_m | 0.5127 | 0.0033 | 0.5068 | 0.5143 |
| geometric | max_lateral_swing_m | 0.6743 | 0.0025 | 0.6727 | 0.6788 |
| geometric | mean_cable_angle_deg | 31.0270 | 0.2054 | 30.6596 | 31.1274 |
| geometric | max_cable_angle_deg | 42.3111 | 0.1948 | 42.1845 | 42.6546 |

## Controller Improvement

| metric | baseline_mean | geometric_mean | improvement_percent |
| --- | --- | --- | --- |
| mean_3d_error_m | 0.4452 | 0.3466 | 22.1486 |
| rms_3d_error_m | 0.4752 | 0.3662 | 22.9435 |
| mean_lateral_swing_m | 0.5641 | 0.5127 | 9.1156 |
| mean_cable_angle_deg | 34.5806 | 31.0270 | 10.2763 |

## Interpretation

All `10` trials completed with valid tracking and payload swing telemetry. The tuned geometric controller remains better than the PX4 position/velocity baseline over the small repeatability set, with lower mean tracking error and lower payload swing-angle metrics.

The GitHub artifact keeps the per-trial summaries, plots, and aggregate CSVs. Raw per-trial telemetry CSVs were omitted from this phase to keep the repository lightweight; the aggregate CSVs preserve the metrics used in this report.

## Next Phase

Scale the repeatability test further only after this dataset is reviewed. A reasonable next step is `10 + 10` trials before attempting another 48-run batch.
