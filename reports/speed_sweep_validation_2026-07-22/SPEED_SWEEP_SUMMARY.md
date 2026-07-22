# Controlled Figure-8 Speed Sweep - 2026-07-22

## Purpose

This experiment checks whether the tuned geometric controller advantage remains visible when the Figure-8 angular rate changes.

## Setup

- Vehicle: `iris_depth_payload`
- Payload: native ball-joint slung payload
- Controllers: PX4 position/velocity baseline and tuned geometric attitude/thrust controller
- Angular rates: `0.15, 0.20, 0.25, 0.30 rad/s`
- Trials per speed and controller: `3`
- Flight duration per trial: `75.0 s`
- Geometric hover thrust: `0.72`
- Validation gates: tracking sample count, PX4 local-position magnitude, steady altitude, and payload swing telemetry
- Raw per-trial telemetry CSV retention: `False`

## Controller Improvement

| omega_rad_s | metric | baseline_mean | geometric_mean | improvement_percent |
| --- | --- | --- | --- | --- |
| 0.1500 | mean_3d_error_m | 0.1788 | 0.2202 | -23.1138 |
| 0.1500 | rms_3d_error_m | 0.1910 | 0.2292 | -20.0196 |
| 0.1500 | mean_lateral_swing_m | 0.3546 | 0.3557 | -0.3070 |
| 0.1500 | mean_cable_angle_deg | 20.8413 | 20.9007 | -0.2849 |
| 0.2000 | mean_3d_error_m | 0.2827 | 0.3127 | -10.6397 |
| 0.2000 | rms_3d_error_m | 0.3006 | 0.3247 | -8.0072 |
| 0.2000 | mean_lateral_swing_m | 0.4634 | 0.4393 | 5.1904 |
| 0.2000 | mean_cable_angle_deg | 27.7412 | 26.1677 | 5.6721 |
| 0.2500 | mean_3d_error_m | 0.4459 | 0.3387 | 24.0418 |
| 0.2500 | rms_3d_error_m | 0.4759 | 0.3543 | 25.5636 |
| 0.2500 | mean_lateral_swing_m | 0.5642 | 0.5147 | 8.7694 |
| 0.2500 | mean_cable_angle_deg | 34.5840 | 31.1520 | 9.9238 |
| 0.3000 | mean_3d_error_m | 0.6760 | 0.3841 | 43.1727 |
| 0.3000 | rms_3d_error_m | 0.7194 | 0.4006 | 44.3094 |
| 0.3000 | mean_lateral_swing_m | 0.6569 | 0.5853 | 10.8903 |
| 0.3000 | mean_cable_angle_deg | 41.4097 | 36.0678 | 12.9001 |

## Profile Metrics

| omega_rad_s | profile | metric | mean | std | min | max |
| --- | --- | --- | --- | --- | --- | --- |
| 0.1500 | baseline | mean_3d_error_m | 0.1788 | 0.0005 | 0.1785 | 0.1794 |
| 0.1500 | baseline | rms_3d_error_m | 0.1910 | 0.0004 | 0.1907 | 0.1914 |
| 0.1500 | baseline | mean_lateral_swing_m | 0.3546 | 0.0000 | 0.3546 | 0.3546 |
| 0.1500 | baseline | mean_cable_angle_deg | 20.8413 | 0.0013 | 20.8401 | 20.8426 |
| 0.1500 | geometric | mean_3d_error_m | 0.2202 | 0.0004 | 0.2199 | 0.2206 |
| 0.1500 | geometric | rms_3d_error_m | 0.2292 | 0.0003 | 0.2289 | 0.2295 |
| 0.1500 | geometric | mean_lateral_swing_m | 0.3557 | 0.0002 | 0.3555 | 0.3559 |
| 0.1500 | geometric | mean_cable_angle_deg | 20.9007 | 0.0090 | 20.8925 | 20.9103 |
| 0.2000 | baseline | mean_3d_error_m | 0.2827 | 0.0007 | 0.2820 | 0.2834 |
| 0.2000 | baseline | rms_3d_error_m | 0.3006 | 0.0009 | 0.2998 | 0.3016 |
| 0.2000 | baseline | mean_lateral_swing_m | 0.4634 | 0.0005 | 0.4627 | 0.4637 |
| 0.2000 | baseline | mean_cable_angle_deg | 27.7412 | 0.0343 | 27.7016 | 27.7622 |
| 0.2000 | geometric | mean_3d_error_m | 0.3127 | 0.0008 | 0.3120 | 0.3136 |
| 0.2000 | geometric | rms_3d_error_m | 0.3247 | 0.0005 | 0.3242 | 0.3252 |
| 0.2000 | geometric | mean_lateral_swing_m | 0.4393 | 0.0007 | 0.4386 | 0.4401 |
| 0.2000 | geometric | mean_cable_angle_deg | 26.1677 | 0.0466 | 26.1198 | 26.2128 |
| 0.2500 | baseline | mean_3d_error_m | 0.4459 | 0.0006 | 0.4453 | 0.4465 |
| 0.2500 | baseline | rms_3d_error_m | 0.4759 | 0.0005 | 0.4755 | 0.4765 |
| 0.2500 | baseline | mean_lateral_swing_m | 0.5642 | 0.0003 | 0.5639 | 0.5644 |
| 0.2500 | baseline | mean_cable_angle_deg | 34.5840 | 0.0153 | 34.5675 | 34.5977 |
| 0.2500 | geometric | mean_3d_error_m | 0.3387 | 0.0013 | 0.3372 | 0.3395 |
| 0.2500 | geometric | rms_3d_error_m | 0.3543 | 0.0012 | 0.3529 | 0.3549 |
| 0.2500 | geometric | mean_lateral_swing_m | 0.5147 | 0.0002 | 0.5145 | 0.5150 |
| 0.2500 | geometric | mean_cable_angle_deg | 31.1520 | 0.0163 | 31.1408 | 31.1707 |
| 0.3000 | baseline | mean_3d_error_m | 0.6760 | 0.0039 | 0.6716 | 0.6791 |
| 0.3000 | baseline | rms_3d_error_m | 0.7194 | 0.0033 | 0.7158 | 0.7223 |
| 0.3000 | baseline | mean_lateral_swing_m | 0.6569 | 0.0006 | 0.6564 | 0.6575 |
| 0.3000 | baseline | mean_cable_angle_deg | 41.4097 | 0.0409 | 41.3792 | 41.4561 |
| 0.3000 | geometric | mean_3d_error_m | 0.3841 | 0.0008 | 0.3833 | 0.3849 |
| 0.3000 | geometric | rms_3d_error_m | 0.4006 | 0.0007 | 0.3999 | 0.4013 |
| 0.3000 | geometric | mean_lateral_swing_m | 0.5853 | 0.0004 | 0.5849 | 0.5857 |
| 0.3000 | geometric | mean_cable_angle_deg | 36.0678 | 0.0311 | 36.0347 | 36.0965 |

## Plots

- `speed_sweep_tracking_swing.png`
- `speed_sweep_improvement.png`

## Interpretation

This is a controlled screening sweep, not a final statistical campaign. It reuses the same validation gates as the repeatability phase and keeps all valid trials in the aggregate.

The main finding is speed dependence. At `omega=0.15 rad/s`, the PX4 baseline tracks better than the geometric controller and both controllers produce nearly identical swing. At `omega=0.20 rad/s`, the PX4 baseline still tracks better, but the geometric controller already reduces payload swing. At `omega=0.25 rad/s` and `omega=0.30 rad/s`, the geometric controller improves both trajectory tracking and payload swing.

The crossover behavior suggests that the current geometric-controller gains are better suited to moderate and high trajectory rates than to slow Figure-8 motion. Slow-speed tuning should therefore be treated separately from high-speed payload-swing suppression.
