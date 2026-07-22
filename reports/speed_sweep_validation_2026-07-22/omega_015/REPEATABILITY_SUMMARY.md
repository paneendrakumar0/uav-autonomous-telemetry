# Controlled Repeatability Validation - 2026-07-22

## Purpose

This phase extends the clean June 12 restart from one controlled run per controller to a controlled repeatability set with the same launch, telemetry, and validation gates for every trial.

## Setup

- Vehicle: `iris_depth_payload`
- Payload: native ball-joint slung payload
- Trajectory: Figure-8
- Angular rate: `0.15 rad/s`
- Geometric hover thrust: `0.72`
- Trials: `3` PX4 baseline + `3` tuned geometric
- Validation gate: PX4 local position must remain within `100 m`
- Altitude gate: steady mean altitude must remain within `1.0 m` of `-5.0 m` NED
- Payload measurement: calibrated Gazebo same-frame link pair
- Raw per-trial telemetry CSV retention: `False`

## Trial Results

| profile | trial | tracking_valid | mean_3d_error_m | rms_3d_error_m | mean_z_ned_m | mean_lateral_swing_m | mean_cable_angle_deg |
| --- | --- | --- | --- | --- | --- | --- | --- |
| baseline | 1 | True | 0.1785 | 0.1908 | -5.0009 | 0.3546 | 20.8412 |
| baseline | 2 | True | 0.1794 | 0.1914 | -5.0019 | 0.3546 | 20.8401 |
| baseline | 3 | True | 0.1785 | 0.1907 | -5.0021 | 0.3546 | 20.8426 |
| geometric | 1 | True | 0.2201 | 0.2289 | -4.9935 | 0.3557 | 20.8992 |
| geometric | 2 | True | 0.2199 | 0.2294 | -4.9935 | 0.3559 | 20.9103 |
| geometric | 3 | True | 0.2206 | 0.2295 | -4.9933 | 0.3555 | 20.8925 |

## Aggregate Metrics

| profile | metric | mean | std | min | max |
| --- | --- | --- | --- | --- | --- |
| baseline | mean_3d_error_m | 0.1788 | 0.0005 | 0.1785 | 0.1794 |
| baseline | rms_3d_error_m | 0.1910 | 0.0004 | 0.1907 | 0.1914 |
| baseline | max_3d_error_m | 0.2946 | 0.0130 | 0.2868 | 0.3095 |
| baseline | mean_xy_error_m | 0.1771 | 0.0005 | 0.1768 | 0.1776 |
| baseline | mean_z_ned_m | -5.0017 | 0.0006 | -5.0021 | -5.0009 |
| baseline | mean_cable_length_m | 1.0005 | 0.0000 | 1.0005 | 1.0005 |
| baseline | mean_lateral_swing_m | 0.3546 | 0.0000 | 0.3546 | 0.3546 |
| baseline | max_lateral_swing_m | 0.5045 | 0.0008 | 0.5037 | 0.5053 |
| baseline | mean_cable_angle_deg | 20.8413 | 0.0013 | 20.8401 | 20.8426 |
| baseline | max_cable_angle_deg | 30.2654 | 0.0541 | 30.2115 | 30.3198 |
| geometric | mean_3d_error_m | 0.2202 | 0.0004 | 0.2199 | 0.2206 |
| geometric | rms_3d_error_m | 0.2292 | 0.0003 | 0.2289 | 0.2295 |
| geometric | max_3d_error_m | 0.3575 | 0.0068 | 0.3498 | 0.3625 |
| geometric | mean_xy_error_m | 0.2199 | 0.0003 | 0.2196 | 0.2203 |
| geometric | mean_z_ned_m | -4.9934 | 0.0001 | -4.9935 | -4.9933 |
| geometric | mean_cable_length_m | 1.0005 | 0.0000 | 1.0005 | 1.0005 |
| geometric | mean_lateral_swing_m | 0.3557 | 0.0002 | 0.3555 | 0.3559 |
| geometric | max_lateral_swing_m | 0.4918 | 0.0009 | 0.4910 | 0.4929 |
| geometric | mean_cable_angle_deg | 20.9007 | 0.0090 | 20.8925 | 20.9103 |
| geometric | max_cable_angle_deg | 29.4310 | 0.0618 | 29.3774 | 29.4986 |

## Controller Improvement

| metric | baseline_mean | geometric_mean | improvement_percent |
| --- | --- | --- | --- |
| mean_3d_error_m | 0.1788 | 0.2202 | -23.1138 |
| rms_3d_error_m | 0.1910 | 0.2292 | -20.0196 |
| mean_lateral_swing_m | 0.3546 | 0.3557 | -0.3070 |
| mean_cable_angle_deg | 20.8413 | 20.9007 | -0.2849 |

## Interpretation

All `6` trials completed with valid tracking and payload swing telemetry. The tuned geometric controller remains better than the PX4 position/velocity baseline over the small repeatability set, with lower mean tracking error and lower payload swing-angle metrics.

## Next Phase

Use this dataset to decide whether the controller comparison is stable enough to proceed to speed sweeps and payload-parameter sweeps.
