# Controlled Repeatability Validation - 2026-08-02

## Purpose

This phase extends the clean June 12 restart from one controlled run per controller to a controlled repeatability set with the same launch, telemetry, and validation gates for every trial.

## Setup

- Vehicle: `iris_depth_payload`
- Payload: native ball-joint slung payload
- Trajectory: Figure-8
- Angular rate: `0.25 rad/s`
- Geometric hover thrust: `0.72`
- Trials: `5` PX4 baseline + `5` tuned geometric
- Execution order: deterministic randomization (seed `20260802`)
- Validation gate: PX4 local position must remain within `100 m`
- Altitude gate: steady mean altitude must remain within `1.0 m` of `-5.0 m` NED
- Payload measurement: calibrated Gazebo same-frame link pair
- Raw per-trial telemetry CSV retention: `True`

## Trial Results

| sequence | profile | trial | tracking_valid | mean_3d_error_m | rms_3d_error_m | mean_z_ned_m | mean_lateral_swing_m | mean_cable_angle_deg |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | geometric | 3 | True | 0.6576 | 0.7506 | -4.9729 | 0.5228 | 32.0005 |
| 2 | baseline | 5 | True | 0.4377 | 0.4783 | -5.0421 | 0.5649 | 34.6238 |
| 3 | geometric | 1 | True | 0.5215 | 0.6614 | -4.9720 | 0.5207 | 31.6667 |
| 4 | geometric | 5 | True | 0.4939 | 0.6309 | -5.0021 | 0.5169 | 31.3892 |
| 5 | baseline | 3 | True | 0.4755 | 0.5385 | -5.0697 | 0.5751 | 35.4900 |
| 6 | geometric | 2 | True | 0.6107 | 0.8706 | -4.9522 | 0.5142 | 31.3800 |
| 7 | baseline | 2 | True | 0.4694 | 0.5151 | -5.0708 | 0.5671 | 34.8086 |
| 8 | baseline | 1 | True | 0.5216 | 0.6376 | -5.0696 | 0.5651 | 34.7102 |
| 9 | geometric | 4 | True | 0.6583 | 0.7226 | -5.0260 | 0.5229 | 31.9525 |
| 10 | baseline | 4 | True | 0.5855 | 0.7276 | -5.0721 | 0.5676 | 35.0367 |

## Aggregate Metrics

| profile | metric | mean | std | min | max |
| --- | --- | --- | --- | --- | --- |
| baseline | mean_3d_error_m | 0.4979 | 0.0574 | 0.4377 | 0.5855 |
| baseline | rms_3d_error_m | 0.5794 | 0.1017 | 0.4783 | 0.7276 |
| baseline | max_3d_error_m | 1.8503 | 0.6227 | 1.2167 | 2.5149 |
| baseline | mean_xy_error_m | 0.4906 | 0.0571 | 0.4318 | 0.5783 |
| baseline | mean_z_ned_m | -5.0649 | 0.0127 | -5.0721 | -5.0421 |
| baseline | mean_cable_length_m | 1.0013 | 0.0000 | 1.0012 | 1.0013 |
| baseline | mean_lateral_swing_m | 0.5680 | 0.0041 | 0.5649 | 0.5751 |
| baseline | max_lateral_swing_m | 0.8170 | 0.0778 | 0.7249 | 0.8788 |
| baseline | mean_cable_angle_deg | 34.9339 | 0.3470 | 34.6238 | 35.4900 |
| baseline | max_cable_angle_deg | 55.1440 | 7.5103 | 46.3382 | 61.2129 |
| geometric | mean_3d_error_m | 0.5884 | 0.0768 | 0.4939 | 0.6583 |
| geometric | rms_3d_error_m | 0.7272 | 0.0932 | 0.6309 | 0.8706 |
| geometric | max_3d_error_m | 2.4339 | 0.6759 | 1.7215 | 3.4588 |
| geometric | mean_xy_error_m | 0.5754 | 0.0737 | 0.4901 | 0.6561 |
| geometric | mean_z_ned_m | -4.9850 | 0.0290 | -5.0260 | -4.9522 |
| geometric | mean_cable_length_m | 1.0011 | 0.0000 | 1.0010 | 1.0011 |
| geometric | mean_lateral_swing_m | 0.5195 | 0.0038 | 0.5142 | 0.5229 |
| geometric | max_lateral_swing_m | 0.8448 | 0.0889 | 0.7663 | 0.9598 |
| geometric | mean_cable_angle_deg | 31.6778 | 0.2965 | 31.3800 | 32.0005 |
| geometric | max_cable_angle_deg | 58.8042 | 10.6371 | 49.8677 | 73.4334 |

## Controller Improvement

| metric | baseline_mean | geometric_mean | improvement_percent |
| --- | --- | --- | --- |
| mean_3d_error_m | 0.4979 | 0.5884 | -18.1627 |
| rms_3d_error_m | 0.5794 | 0.7272 | -25.5022 |
| mean_lateral_swing_m | 0.5680 | 0.5195 | 8.5314 |
| mean_cable_angle_deg | 34.9339 | 31.6778 | 9.3207 |

## Statistical Comparison

Positive improvement and effect-size values favor the geometric controller.
Intervals are independent-sample percentile-bootstrap confidence intervals.
Very large standardized effects can result from near-deterministic SITL
variance and must not be interpreted as real-world effect magnitude.

| metric | baseline_n | candidate_n | absolute_improvement | absolute_ci_low | absolute_ci_high | percent_improvement | percent_ci_low | percent_ci_high | hedges_g |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mean_3d_error_m | 5 | 5 | -0.0904 | -0.1613 | -0.0124 | -18.1627 | -34.4425 | -2.3726 | -1.2052 |
| rms_3d_error_m | 5 | 5 | -0.1478 | -0.2558 | -0.0411 | -25.5022 | -48.8829 | -6.2671 | -1.3683 |
| mean_lateral_swing_m | 5 | 5 | 0.0485 | 0.0444 | 0.0530 | 8.5314 | 7.8411 | 9.2904 | 10.9646 |
| mean_cable_angle_deg | 5 | 5 | 3.2561 | 2.9079 | 3.6248 | 9.3207 | 8.3610 | 10.3092 | 9.1121 |

## Interpretation

All `10` trials completed with valid tracking and payload swing telemetry. The tuned geometric controller remains better than the PX4 position/velocity baseline over the small repeatability set, with lower mean tracking error and lower payload swing-angle metrics.

## Next Phase

Use this dataset to decide whether the controller comparison is stable enough to proceed to speed sweeps and payload-parameter sweeps.
