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
- Crosswind speeds represented in this envelope: `0.0, 2.5, 5.0, 7.5, 10.0 m/s`
- Existing screening imports enabled: `True`
- Raw per-trial telemetry retention: `False`

## Disturbance Cases

| label | type | speed_m_s | world | source |
| --- | --- | --- | --- | --- |
| crosswind_y5 | crosswind_y | 5.0000 | payload_crosswind_y5 | reports/wind_disturbance_crosswind_y5_2026-07-25 |
| gust_y10 | gust_y | 10.0000 | payload_gust_y10 | reports/wind_disturbance_gust_y10_2026-07-25 |
| updraft_z5 | updraft_z | 5.0000 | payload_updraft_z5 | reports/wind_disturbance_updraft_z5_2026-07-25 |
| crosswind_y0 | crosswind_y | 0.0000 | payload_crosswind_y0 | generated_run |
| crosswind_y2p5 | crosswind_y | 2.5000 | payload_crosswind_y2p5 | generated_run |
| crosswind_y7p5 | crosswind_y | 7.5000 | payload_crosswind_y7p5 | generated_run |
| crosswind_y10 | crosswind_y | 10.0000 | payload_crosswind_y10 | generated_run |

## Profile Metrics

| case | profile | tracking_valid | mean_3d_error_m | rms_3d_error_m | mean_lateral_swing_m | mean_cable_angle_deg | tracking_reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| crosswind_y0 | baseline | True | 0.4432 | 0.4735 | 0.5644 | 34.6004 | valid tracking telemetry |
| crosswind_y0 | geometric | True | 0.3354 | 0.3514 | 0.5138 | 31.0947 | valid tracking telemetry |
| crosswind_y2p5 | baseline | True | 0.4438 | 0.4739 | 0.5641 | 34.5743 | valid tracking telemetry |
| crosswind_y2p5 | geometric | True | 0.6491 | 0.6945 | 0.5144 | 31.1333 | valid tracking telemetry |
| crosswind_y5 | baseline | True | 0.4467 | 0.4782 | 0.5662 | 34.7045 | valid tracking telemetry |
| crosswind_y5 | geometric | True | 1.2690 | 1.3013 | 0.5139 | 31.0788 | valid tracking telemetry |
| crosswind_y7p5 | baseline | True | 0.4502 | 0.4808 | 0.5647 | 34.6168 | valid tracking telemetry |
| crosswind_y7p5 | geometric | True | 1.9210 | 1.9408 | 0.5145 | 31.1359 | valid tracking telemetry |
| crosswind_y10 | baseline | True | 0.4574 | 0.4871 | 0.5644 | 34.6009 | valid tracking telemetry |
| crosswind_y10 | geometric | True | 2.5982 | 2.6141 | 0.5139 | 31.0984 | valid tracking telemetry |
| gust_y10 | baseline | True | 0.5427 | 0.6266 | 0.5646 | 34.5853 | valid tracking telemetry |
| gust_y10 | geometric | True | 0.4554 | 0.6022 | 0.5275 | 32.0458 | valid tracking telemetry |
| updraft_z5 | baseline | False | 6.3698 | 6.4120 | 0.0000 | 0.0018 | mean altitude error too large (5.02 m > 1.50 m) |
| updraft_z5 | geometric | True | 0.8452 | 0.8514 | 0.5214 | 31.6028 | valid tracking telemetry |

## Controller Comparison

| case | metric | baseline | geometric | both_tracking_valid | improvement_percent |
| --- | --- | --- | --- | --- | --- |
| crosswind_y0 | mean_3d_error_m | 0.4432 | 0.3354 | True | 24.3083 |
| crosswind_y0 | mean_cable_angle_deg | 34.6004 | 31.0947 | True | 10.1319 |
| crosswind_y0 | mean_lateral_swing_m | 0.5644 | 0.5138 | True | 8.9740 |
| crosswind_y0 | rms_3d_error_m | 0.4735 | 0.3514 | True | 25.7771 |
| crosswind_y2p5 | mean_3d_error_m | 0.4438 | 0.6491 | True | -46.2524 |
| crosswind_y2p5 | mean_cable_angle_deg | 34.5743 | 31.1333 | True | 9.9523 |
| crosswind_y2p5 | mean_lateral_swing_m | 0.5641 | 0.5144 | True | 8.8044 |
| crosswind_y2p5 | rms_3d_error_m | 0.4739 | 0.6945 | True | -46.5517 |
| crosswind_y5 | mean_3d_error_m | 0.4467 | 1.2690 | True | -184.0795 |
| crosswind_y5 | mean_cable_angle_deg | 34.7045 | 31.0788 | True | 10.4475 |
| crosswind_y5 | mean_lateral_swing_m | 0.5662 | 0.5139 | True | 9.2335 |
| crosswind_y5 | rms_3d_error_m | 0.4782 | 1.3013 | True | -172.1080 |
| crosswind_y7p5 | mean_3d_error_m | 0.4502 | 1.9210 | True | -326.7135 |
| crosswind_y7p5 | mean_cable_angle_deg | 34.6168 | 31.1359 | True | 10.0556 |
| crosswind_y7p5 | mean_lateral_swing_m | 0.5647 | 0.5145 | True | 8.8878 |
| crosswind_y7p5 | rms_3d_error_m | 0.4808 | 1.9408 | True | -303.6711 |
| crosswind_y10 | mean_3d_error_m | 0.4574 | 2.5982 | True | -467.9925 |
| crosswind_y10 | mean_cable_angle_deg | 34.6009 | 31.0984 | True | 10.1227 |
| crosswind_y10 | mean_lateral_swing_m | 0.5644 | 0.5139 | True | 8.9568 |
| crosswind_y10 | rms_3d_error_m | 0.4871 | 2.6141 | True | -436.6271 |
| gust_y10 | mean_3d_error_m | 0.5427 | 0.4554 | True | 16.0770 |
| gust_y10 | mean_cable_angle_deg | 34.5853 | 32.0458 | True | 7.3427 |
| gust_y10 | mean_lateral_swing_m | 0.5646 | 0.5275 | True | 6.5663 |
| gust_y10 | rms_3d_error_m | 0.6266 | 0.6022 | True | 3.8981 |
| updraft_z5 | mean_3d_error_m | 6.3698 | 0.8452 | False | n/a |
| updraft_z5 | mean_cable_angle_deg | 0.0018 | 31.6028 | False | n/a |
| updraft_z5 | mean_lateral_swing_m | 0.0000 | 0.5214 | False | n/a |
| updraft_z5 | rms_3d_error_m | 6.4120 | 0.8514 | False | n/a |

## Plots

- `wind_envelope_tracking_error.png`
- `wind_envelope_payload_swing.png`
- `wind_envelope_improvement.png`

## Interpretation

The completed crosswind envelope shows a clear controller tradeoff. In clean air, the geometric controller improves mean 3D tracking error by roughly `24%` and reduces mean cable angle by roughly `10%`. Once a constant Y-crosswind is introduced, the swing benefit remains nearly constant at about `9-10%`, but trajectory tracking degrades sharply. The geometric controller is already worse than PX4 at `2.5 m/s`, reaches `1.269 m` mean 3D error at `5 m/s`, and reaches `2.598 m` at `10 m/s`.

The PX4 position/velocity baseline remains near `0.44-0.46 m` mean 3D error across the tested constant-crosswind range. This suggests PX4 handles the steady wind bias better for path tracking, while the geometric controller is still better at suppressing payload swing. The gust and updraft cases remain important boundary evidence: under the finite Y-gust, geometric control improves average tracking and swing but has larger peak excursions; under vertical updraft, PX4 baseline fails the altitude validation gate while the geometric controller completes the circuit with altitude bias.
