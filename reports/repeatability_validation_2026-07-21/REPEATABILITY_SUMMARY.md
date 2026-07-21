# Controlled Repeatability Validation - 2026-07-21

## Purpose

This phase extends the clean June 12 restart from one controlled run per controller to a small repeatability set. It intentionally uses only three trials per controller before any larger batch testing.

## Setup

- Vehicle: `iris_depth_payload`
- Payload: native ball-joint slung payload
- Trajectory: Figure-8
- Angular rate: `0.25 rad/s`
- Geometric hover thrust: `0.72`
- Trials: `3` PX4 baseline + `3` tuned geometric
- Validation gate: PX4 local position must remain within `100 m`
- Payload measurement: calibrated Gazebo same-frame link pair

## Trial Results

| profile | trial | tracking_valid | mean_3d_error_m | rms_3d_error_m | mean_z_ned_m | mean_lateral_swing_m | mean_cable_angle_deg |
| --- | --- | --- | --- | --- | --- | --- | --- |
| baseline | 1 | True | 0.4446 | 0.4749 | -4.9989 | 0.5644 | 34.5947 |
| baseline | 2 | True | 0.4448 | 0.4755 | -4.9988 | 0.5642 | 34.5834 |
| baseline | 3 | True | 0.4449 | 0.4756 | -4.9985 | 0.5647 | 34.6156 |
| geometric | 1 | True | 0.3409 | 0.3558 | -4.9946 | 0.5146 | 31.1483 |
| geometric | 2 | True | 0.3387 | 0.3539 | -4.9945 | 0.5141 | 31.1145 |
| geometric | 3 | True | 0.3382 | 0.3531 | -4.9940 | 0.5151 | 31.1804 |

## Aggregate Metrics

| profile | metric | mean | std | min | max |
| --- | --- | --- | --- | --- | --- |
| baseline | mean_3d_error_m | 0.4447 | 0.0001 | 0.4446 | 0.4449 |
| baseline | rms_3d_error_m | 0.4753 | 0.0004 | 0.4749 | 0.4756 |
| baseline | max_3d_error_m | 0.6698 | 0.0065 | 0.6623 | 0.6743 |
| baseline | mean_xy_error_m | 0.4444 | 0.0001 | 0.4443 | 0.4445 |
| baseline | mean_z_ned_m | -4.9988 | 0.0002 | -4.9989 | -4.9985 |
| baseline | mean_cable_length_m | 1.0012 | 0.0000 | 1.0012 | 1.0012 |
| baseline | mean_lateral_swing_m | 0.5644 | 0.0002 | 0.5642 | 0.5647 |
| baseline | max_lateral_swing_m | 0.7305 | 0.0008 | 0.7295 | 0.7310 |
| baseline | mean_cable_angle_deg | 34.5979 | 0.0163 | 34.5834 | 34.6156 |
| baseline | max_cable_angle_deg | 46.7988 | 0.0690 | 46.7198 | 46.8469 |
| geometric | mean_3d_error_m | 0.3392 | 0.0015 | 0.3382 | 0.3409 |
| geometric | rms_3d_error_m | 0.3543 | 0.0014 | 0.3531 | 0.3558 |
| geometric | max_3d_error_m | 0.5773 | 0.0025 | 0.5755 | 0.5802 |
| geometric | mean_xy_error_m | 0.3390 | 0.0015 | 0.3379 | 0.3407 |
| geometric | mean_z_ned_m | -4.9944 | 0.0003 | -4.9946 | -4.9940 |
| geometric | mean_cable_length_m | 1.0010 | 0.0000 | 1.0010 | 1.0010 |
| geometric | mean_lateral_swing_m | 0.5146 | 0.0005 | 0.5141 | 0.5151 |
| geometric | max_lateral_swing_m | 0.6731 | 0.0014 | 0.6716 | 0.6742 |
| geometric | mean_cable_angle_deg | 31.1477 | 0.0330 | 31.1145 | 31.1804 |
| geometric | max_cable_angle_deg | 42.2183 | 0.1039 | 42.1003 | 42.2959 |

## Controller Improvement

| metric | baseline_mean | geometric_mean | improvement_percent |
| --- | --- | --- | --- |
| mean_3d_error_m | 0.4447 | 0.3392 | 23.7207 |
| rms_3d_error_m | 0.4753 | 0.3543 | 25.4645 |
| mean_lateral_swing_m | 0.5644 | 0.5146 | 8.8264 |
| mean_cable_angle_deg | 34.5979 | 31.1477 | 9.9722 |

## Interpretation

All `6` trials completed with valid tracking and payload swing telemetry. The tuned geometric controller remains better than the PX4 position/velocity baseline over the small repeatability set, with lower mean tracking error and lower payload swing-angle metrics.

## Next Phase

Scale the repeatability test to a larger sample only after this six-run dataset is reviewed. A reasonable next step is `5 + 5` or `10 + 10` trials before attempting another 48-run batch.
