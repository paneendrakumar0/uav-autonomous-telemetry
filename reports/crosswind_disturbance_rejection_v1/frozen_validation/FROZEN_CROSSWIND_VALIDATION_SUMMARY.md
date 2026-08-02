# Frozen Crosswind Candidate Validation - 2026-08-02

## Protocol

- Candidate gains: `ki_xy=0.35`, `kd_xy=1.3`
- Winds: `0, 5, 10 m/s`
- Trials: `5` per controller per wind
- Total official flights: `30`
- Randomized-order seed: `20260803`
- Bootstrap confidence: `95%` with `10000` resamples
- Raw telemetry retained: `true`

## Aggregate Metrics

| speed_m_s | profile | metric | n | mean | std | min | max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | baseline | mean_3d_error_m | 5 | 0.4388 | 0.0207 | 0.4122 | 0.4684 |
| 0.0000 | baseline | rms_3d_error_m | 5 | 0.4720 | 0.0246 | 0.4377 | 0.5067 |
| 0.0000 | baseline | max_3d_error_m | 5 | 0.9854 | 0.3036 | 0.6444 | 1.4223 |
| 0.0000 | baseline | mean_lateral_swing_m | 5 | 0.5613 | 0.0033 | 0.5562 | 0.5645 |
| 0.0000 | baseline | mean_cable_angle_deg | 5 | 34.3827 | 0.2246 | 34.0179 | 34.5736 |
| 0.0000 | geometric | mean_3d_error_m | 5 | 0.4895 | 0.0902 | 0.4116 | 0.6420 |
| 0.0000 | geometric | rms_3d_error_m | 5 | 0.6187 | 0.2569 | 0.4454 | 1.0718 |
| 0.0000 | geometric | max_3d_error_m | 5 | 1.8694 | 1.6237 | 0.8765 | 4.7156 |
| 0.0000 | geometric | mean_lateral_swing_m | 5 | 0.5363 | 0.0024 | 0.5323 | 0.5389 |
| 0.0000 | geometric | mean_cable_angle_deg | 5 | 32.7826 | 0.2815 | 32.3797 | 33.1678 |
| 5.0000 | baseline | mean_3d_error_m | 5 | 0.4512 | 0.0226 | 0.4270 | 0.4760 |
| 5.0000 | baseline | rms_3d_error_m | 5 | 0.4877 | 0.0357 | 0.4526 | 0.5394 |
| 5.0000 | baseline | max_3d_error_m | 5 | 1.1057 | 0.3409 | 0.6638 | 1.5351 |
| 5.0000 | baseline | mean_lateral_swing_m | 5 | 0.5632 | 0.0014 | 0.5612 | 0.5651 |
| 5.0000 | baseline | mean_cable_angle_deg | 5 | 34.5413 | 0.1425 | 34.3518 | 34.7380 |
| 5.0000 | geometric | mean_3d_error_m | 5 | 0.5025 | 0.0717 | 0.4195 | 0.5889 |
| 5.0000 | geometric | rms_3d_error_m | 5 | 0.5945 | 0.1387 | 0.4595 | 0.7892 |
| 5.0000 | geometric | max_3d_error_m | 5 | 1.5429 | 0.9378 | 0.8342 | 3.0770 |
| 5.0000 | geometric | mean_lateral_swing_m | 5 | 0.5371 | 0.0050 | 0.5302 | 0.5433 |
| 5.0000 | geometric | mean_cable_angle_deg | 5 | 32.7542 | 0.3802 | 32.2556 | 33.2286 |
| 10.0000 | baseline | mean_3d_error_m | 5 | 0.4762 | 0.0176 | 0.4618 | 0.5068 |
| 10.0000 | baseline | rms_3d_error_m | 5 | 0.5018 | 0.0145 | 0.4875 | 0.5245 |
| 10.0000 | baseline | max_3d_error_m | 5 | 0.8809 | 0.2026 | 0.7129 | 1.1442 |
| 10.0000 | baseline | mean_lateral_swing_m | 5 | 0.5639 | 0.0020 | 0.5621 | 0.5673 |
| 10.0000 | baseline | mean_cable_angle_deg | 5 | 34.5540 | 0.1266 | 34.4266 | 34.7658 |
| 10.0000 | geometric | mean_3d_error_m | 5 | 1.4345 | 0.0313 | 1.3962 | 1.4775 |
| 10.0000 | geometric | rms_3d_error_m | 5 | 1.4843 | 0.0294 | 1.4436 | 1.5238 |
| 10.0000 | geometric | max_3d_error_m | 5 | 2.2329 | 0.1643 | 2.1073 | 2.5081 |
| 10.0000 | geometric | mean_lateral_swing_m | 5 | 0.5270 | 0.0025 | 0.5235 | 0.5292 |
| 10.0000 | geometric | mean_cable_angle_deg | 5 | 32.0607 | 0.1856 | 31.7965 | 32.2440 |

## Statistical Comparison

Positive improvement favors the frozen geometric candidate.

| speed_m_s | metric | absolute_improvement | absolute_ci_low | absolute_ci_high | percent_improvement | percent_ci_low | percent_ci_high | hedges_g |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0000 | mean_3d_error_m | -0.0507 | -0.1314 | 0.0102 | -11.5588 | -30.0880 | 2.2951 | -0.6998 |
| 0.0000 | rms_3d_error_m | -0.1467 | -0.3780 | -0.0016 | -31.0901 | -80.5120 | -0.3455 | -0.7262 |
| 0.0000 | max_3d_error_m | -0.8840 | -2.3696 | 0.0986 | -89.7071 | -256.1301 | 8.4749 | -0.6836 |
| 0.0000 | mean_lateral_swing_m | 0.0251 | 0.0218 | 0.0282 | 4.4632 | 3.9049 | 5.0046 | 7.8898 |
| 0.0000 | mean_cable_angle_deg | 1.6001 | 1.3093 | 1.8789 | 4.6538 | 3.8225 | 5.4497 | 5.6754 |
| 5.0000 | mean_3d_error_m | -0.0512 | -0.1075 | 0.0068 | -11.3551 | -24.2139 | 1.5038 | -0.8708 |
| 5.0000 | rms_3d_error_m | -0.1068 | -0.2290 | -0.0009 | -21.8966 | -47.7620 | -0.1686 | -0.9522 |
| 5.0000 | max_3d_error_m | -0.4372 | -1.2831 | 0.2590 | -39.5424 | -127.8577 | 21.0005 | -0.5597 |
| 5.0000 | mean_lateral_swing_m | 0.0262 | 0.0223 | 0.0302 | 4.6489 | 3.9506 | 5.3580 | 6.4517 |
| 5.0000 | mean_cable_angle_deg | 1.7871 | 1.4694 | 2.1090 | 5.1738 | 4.2594 | 6.0993 | 5.6215 |
| 10.0000 | mean_3d_error_m | -0.9583 | -0.9856 | -0.9299 | -201.2186 | -210.2089 | -190.5185 | -34.0646 |
| 10.0000 | rms_3d_error_m | -0.9826 | -1.0075 | -0.9565 | -195.8182 | -203.5152 | -187.3567 | -38.2579 |
| 10.0000 | max_3d_error_m | -1.3520 | -1.5521 | -1.1529 | -153.4878 | -208.2405 | -111.6059 | -6.6207 |
| 10.0000 | mean_lateral_swing_m | 0.0369 | 0.0345 | 0.0395 | 6.5381 | 6.1339 | 6.9862 | 14.7685 |
| 10.0000 | mean_cable_angle_deg | 2.4933 | 2.3269 | 2.6776 | 7.2157 | 6.7451 | 7.7373 | 14.1734 |

## Interpretation Rule

The candidate is successful only where tracking improves without eliminating the payload-angle benefit. Negative or inconclusive results are retained and reported; this evaluation does not permit gain changes.
