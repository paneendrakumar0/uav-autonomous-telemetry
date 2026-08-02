# Remaining 32-Run Validation Matrix - 2026-08-02

## Protocol

- Deterministic randomized run-order seed: `20260802`
- Flight duration: `75.0 s`
- Profiles: PX4 baseline and geometric attitude/thrust
- Families: 10 wind, 6 altitude, 6 speed, 6 payload-mass, 4 gust/updraft runs
- Raw telemetry retained: `true`
- Completed valid runs: `32/32`

## Per-run Metrics

| sequence | family | case | profile | tracking_valid | swing_valid | mean_3d_error_m | mean_cable_angle_deg |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | speed | omega_020 | baseline | True | True | 0.3881 | 28.6028 |
| 12 | wind | crosswind_y5 | baseline | True | True | 0.4826 | 34.6758 |
| 13 | altitude | altitude_5m | baseline | True | True | 0.4696 | 34.7026 |
| 14 | stress | updraft_z5 | baseline | True | True | 0.6514 | 35.4124 |
| 15 | payload | mass_100g | baseline | True | True | 0.5201 | 34.9345 |
| 16 | wind | crosswind_y5 | geometric | True | True | 1.3516 | 30.9937 |
| 17 | stress | updraft_z5 | geometric | True | True | 0.9645 | 31.2181 |
| 18 | altitude | altitude_3m | baseline | True | True | 0.5294 | 35.1784 |
| 19 | wind | crosswind_y0 | geometric | True | True | 0.4851 | 31.4829 |
| 20 | altitude | altitude_5m | geometric | True | True | 0.5475 | 32.3210 |
| 21 | wind | crosswind_y7p5 | geometric | True | True | 1.9856 | 31.8988 |
| 22 | wind | crosswind_y2p5 | baseline | True | True | 0.5433 | 34.6891 |
| 23 | stress | gust_y10 | geometric | True | True | 0.5480 | 30.5060 |
| 24 | payload | mass_050g | geometric | True | True | 0.5842 | 32.1043 |
| 25 | payload | mass_050g | baseline | True | True | 0.5458 | 35.3673 |
| 26 | speed | omega_025 | baseline | True | True | 0.4735 | 34.6820 |
| 27 | speed | omega_030 | baseline | True | True | 0.7158 | 40.9093 |
| 28 | altitude | altitude_3m | geometric | True | True | 0.4382 | 31.5365 |
| 29 | payload | mass_200g | geometric | True | True | 0.7683 | 29.0330 |
| 30 | speed | omega_030 | geometric | True | True | 0.5903 | 36.4762 |
| 31 | wind | crosswind_y2p5 | geometric | True | True | 0.7363 | 31.9093 |
| 32 | payload | mass_200g | baseline | True | True | 0.6130 | 34.3409 |
| 33 | wind | crosswind_y10 | baseline | True | True | 0.5994 | 35.3613 |
| 34 | altitude | altitude_7m | geometric | True | True | 0.5326 | 31.8067 |
| 35 | speed | omega_025 | geometric | True | True | 0.5258 | 31.6790 |
| 36 | payload | mass_100g | geometric | True | True | 0.6819 | 30.9053 |
| 37 | wind | crosswind_y10 | geometric | True | True | 2.6432 | 31.0107 |
| 38 | stress | gust_y10 | baseline | True | True | 0.5291 | 35.0650 |
| 39 | wind | crosswind_y7p5 | baseline | True | True | 0.5583 | 35.5215 |
| 40 | wind | crosswind_y0 | baseline | True | True | 0.4512 | 34.7011 |
| 41 | speed | omega_020 | geometric | True | True | 0.3478 | 26.6105 |
| 42 | altitude | altitude_7m | baseline | True | True | 0.4346 | 34.4709 |

## Paired Controller Comparison

Positive improvement favors the geometric controller.

| family | case | metric | baseline | geometric | improvement_percent |
| --- | --- | --- | --- | --- | --- |
| speed | omega_020 | mean_3d_error_m | 0.3881 | 0.3478 | 10.3847 |
| speed | omega_020 | mean_cable_angle_deg | 28.6028 | 26.6105 | 6.9653 |
| wind | crosswind_y5 | mean_3d_error_m | 0.4826 | 1.3516 | -180.0381 |
| wind | crosswind_y5 | mean_cable_angle_deg | 34.6758 | 30.9937 | 10.6188 |
| altitude | altitude_5m | mean_3d_error_m | 0.4696 | 0.5475 | -16.5835 |
| altitude | altitude_5m | mean_cable_angle_deg | 34.7026 | 32.3210 | 6.8629 |
| stress | updraft_z5 | mean_3d_error_m | 0.6514 | 0.9645 | -48.0736 |
| stress | updraft_z5 | mean_cable_angle_deg | 35.4124 | 31.2181 | 11.8442 |
| payload | mass_100g | mean_3d_error_m | 0.5201 | 0.6819 | -31.1058 |
| payload | mass_100g | mean_cable_angle_deg | 34.9345 | 30.9053 | 11.5335 |
| altitude | altitude_3m | mean_3d_error_m | 0.5294 | 0.4382 | 17.2304 |
| altitude | altitude_3m | mean_cable_angle_deg | 35.1784 | 31.5365 | 10.3528 |
| wind | crosswind_y0 | mean_3d_error_m | 0.4512 | 0.4851 | -7.5260 |
| wind | crosswind_y0 | mean_cable_angle_deg | 34.7011 | 31.4829 | 9.2741 |
| wind | crosswind_y7p5 | mean_3d_error_m | 0.5583 | 1.9856 | -255.6237 |
| wind | crosswind_y7p5 | mean_cable_angle_deg | 35.5215 | 31.8988 | 10.1984 |
| wind | crosswind_y2p5 | mean_3d_error_m | 0.5433 | 0.7363 | -35.5156 |
| wind | crosswind_y2p5 | mean_cable_angle_deg | 34.6891 | 31.9093 | 8.0134 |
| stress | gust_y10 | mean_3d_error_m | 0.5291 | 0.5480 | -3.5811 |
| stress | gust_y10 | mean_cable_angle_deg | 35.0650 | 30.5060 | 13.0014 |
| payload | mass_050g | mean_3d_error_m | 0.5458 | 0.5842 | -7.0315 |
| payload | mass_050g | mean_cable_angle_deg | 35.3673 | 32.1043 | 9.2262 |
| speed | omega_025 | mean_3d_error_m | 0.4735 | 0.5258 | -11.0461 |
| speed | omega_025 | mean_cable_angle_deg | 34.6820 | 31.6790 | 8.6588 |
| speed | omega_030 | mean_3d_error_m | 0.7158 | 0.5903 | 17.5293 |
| speed | omega_030 | mean_cable_angle_deg | 40.9093 | 36.4762 | 10.8364 |
| payload | mass_200g | mean_3d_error_m | 0.6130 | 0.7683 | -25.3374 |
| payload | mass_200g | mean_cable_angle_deg | 34.3409 | 29.0330 | 15.4565 |
| wind | crosswind_y10 | mean_3d_error_m | 0.5994 | 2.6432 | -341.0115 |
| wind | crosswind_y10 | mean_cable_angle_deg | 35.3613 | 31.0107 | 12.3032 |
| altitude | altitude_7m | mean_3d_error_m | 0.4346 | 0.5326 | -22.5518 |
| altitude | altitude_7m | mean_cable_angle_deg | 34.4709 | 31.8067 | 7.7289 |
