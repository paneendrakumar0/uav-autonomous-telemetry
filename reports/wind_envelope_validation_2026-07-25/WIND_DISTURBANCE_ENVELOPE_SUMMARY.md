# Wind Disturbance Envelope Screening - 2026-07-25

## Purpose

This phase turns the first wind tests into a repeatable disturbance-envelope workflow. The objective is to evaluate how the PX4 position/velocity baseline and the tuned geometric attitude/thrust controller degrade under external aerodynamic disturbance.

## Setup

- Vehicle: `iris_depth_payload`
- Payload: nominal `0.05 kg`, `1.0 m` cable
- Trajectory: Figure-8
- Angular rate: `0.25 rad/s`
- Controllers: PX4 position/velocity baseline and tuned geometric attitude/thrust controller
- Constant crosswind direction: `[0.0, 1.0, 0.0]`
- Crosswind speeds prepared for the envelope: `0.0, 2.5, 5.0, 7.5, 10.0 m/s`
- Existing screening imports enabled: `True`
- Raw per-trial telemetry retention: `False`

## Disturbance Cases

| label | type | speed_m_s | world | source |
| --- | --- | --- | --- | --- |
| crosswind_y5 | crosswind_y | 5.0000 | payload_crosswind_y5 | reports/wind_disturbance_crosswind_y5_2026-07-25 |
| gust_y10 | gust_y | 10.0000 | payload_gust_y10 | reports/wind_disturbance_gust_y10_2026-07-25 |
| updraft_z5 | updraft_z | 5.0000 | payload_updraft_z5 | reports/wind_disturbance_updraft_z5_2026-07-25 |

## Profile Metrics

| case | profile | tracking_valid | mean_3d_error_m | rms_3d_error_m | mean_lateral_swing_m | mean_cable_angle_deg | tracking_reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| crosswind_y5 | baseline | True | 0.4467 | 0.4782 | 0.5662 | 34.7045 | valid tracking telemetry |
| crosswind_y5 | geometric | True | 1.2690 | 1.3013 | 0.5139 | 31.0788 | valid tracking telemetry |
| gust_y10 | baseline | True | 0.5427 | 0.6266 | 0.5646 | 34.5853 | valid tracking telemetry |
| gust_y10 | geometric | True | 0.4554 | 0.6022 | 0.5275 | 32.0458 | valid tracking telemetry |
| updraft_z5 | baseline | False | 6.3698 | 6.4120 | 0.0000 | 0.0018 | mean altitude error too large (5.02 m > 1.50 m) |
| updraft_z5 | geometric | True | 0.8452 | 0.8514 | 0.5214 | 31.6028 | valid tracking telemetry |

## Controller Comparison

| case | metric | baseline | geometric | both_tracking_valid | improvement_percent |
| --- | --- | --- | --- | --- | --- |
| crosswind_y5 | mean_3d_error_m | 0.4467 | 1.2690 | True | -184.0795 |
| crosswind_y5 | rms_3d_error_m | 0.4782 | 1.3013 | True | -172.1080 |
| crosswind_y5 | mean_lateral_swing_m | 0.5662 | 0.5139 | True | 9.2335 |
| crosswind_y5 | mean_cable_angle_deg | 34.7045 | 31.0788 | True | 10.4475 |
| gust_y10 | mean_3d_error_m | 0.5427 | 0.4554 | True | 16.0770 |
| gust_y10 | rms_3d_error_m | 0.6266 | 0.6022 | True | 3.8981 |
| gust_y10 | mean_lateral_swing_m | 0.5646 | 0.5275 | True | 6.5663 |
| gust_y10 | mean_cable_angle_deg | 34.5853 | 32.0458 | True | 7.3427 |
| updraft_z5 | mean_3d_error_m | 6.3698 | 0.8452 | False | n/a |
| updraft_z5 | rms_3d_error_m | 6.4120 | 0.8514 | False | n/a |
| updraft_z5 | mean_lateral_swing_m | 0.0000 | 0.5214 | False | n/a |
| updraft_z5 | mean_cable_angle_deg | 0.0018 | 31.6028 | False | n/a |

## Plots

- `wind_envelope_tracking_error.png`
- `wind_envelope_payload_swing.png`
- `wind_envelope_improvement.png`

## Interpretation

The current wind evidence shows that the controller tradeoff is disturbance-dependent. Under constant Y-crosswind, the geometric controller reduces payload swing but loses substantial path-tracking accuracy relative to PX4. Under a finite Y-gust, it improves average tracking and swing but produces larger peak excursions. Under vertical updraft, PX4 baseline fails the altitude validation gate while the geometric controller completes the circuit with altitude bias.

This is now ready to expand into a true envelope campaign by filling the generated constant-crosswind worlds at multiple wind speeds. The important research question for the next batch is not whether the vehicle flies once, but where each controller crosses from acceptable tracking into degraded or failed behavior.
