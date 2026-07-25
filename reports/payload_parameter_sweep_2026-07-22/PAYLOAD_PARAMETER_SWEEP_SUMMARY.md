# Payload Parameter Screening Sweep - 2026-07-25

## Purpose

This screening phase checks whether the controller comparison remains valid when the physical slung payload parameters change. It intentionally varies one physical parameter at a time around the previously validated nominal case.

## Setup

- Vehicle: `iris_depth_payload`
- Trajectory: Figure-8
- Angular rate: `0.25 rad/s`
- Controllers: PX4 position/velocity baseline and tuned geometric attitude/thrust controller
- Payload model: native ball-joint `base_link -> slung_payload`
- Payload radius: `0.1 m`
- Trials per case and controller: `1`
- Raw telemetry retention: `False`
- Live PX4 SDF restored after the sweep: `true`

## Cases

| label | mass_kg | cable_length_m | reason |
| --- | --- | --- | --- |
| nominal_m050_l100 | 0.0500 | 1.0000 | validated nominal payload |
| mass_m100_l100 | 0.1000 | 1.0000 | double payload mass |
| mass_m200_l100 | 0.2000 | 1.0000 | quadruple payload mass |
| cable_m050_l050 | 0.0500 | 0.5000 | short cable |
| cable_m050_l150 | 0.0500 | 1.5000 | long cable |

## Profile Metrics

| case | profile | tracking_valid | swing_valid | mean_3d_error_m | rms_3d_error_m | mean_lateral_swing_m | mean_cable_angle_deg |
| --- | --- | --- | --- | --- | --- | --- | --- |
| nominal_m050_l100 | baseline | True | True | 0.4458 | 0.4755 | 0.5631 | 34.5050 |
| nominal_m050_l100 | geometric | True | True | 0.3358 | 0.3504 | 0.5144 | 31.1301 |
| mass_m100_l100 | baseline | True | True | 0.4915 | 0.5236 | 0.5648 | 34.6221 |
| mass_m100_l100 | geometric | True | True | 0.4691 | 0.4863 | 0.5087 | 30.7442 |
| mass_m200_l100 | baseline | True | True | 0.5908 | 0.6266 | 0.5633 | 34.4996 |
| mass_m200_l100 | geometric | True | True | 0.7424 | 0.7626 | 0.4937 | 29.7272 |
| cable_m050_l050 | baseline | True | True | 0.4489 | 0.4804 | 0.2833 | 34.7595 |
| cable_m050_l050 | geometric | True | True | 0.3568 | 0.3720 | 0.2576 | 31.1943 |
| cable_m050_l150 | baseline | True | True | 0.4334 | 0.4635 | 0.8436 | 34.3972 |
| cable_m050_l150 | geometric | True | True | 0.3497 | 0.3657 | 0.7668 | 30.8706 |

## Controller Comparison

| case | metric | baseline | geometric | improvement_percent |
| --- | --- | --- | --- | --- |
| cable_m050_l050 | mean_3d_error_m | 0.4489 | 0.3568 | 20.5181 |
| cable_m050_l050 | rms_3d_error_m | 0.4804 | 0.3720 | 22.5565 |
| cable_m050_l050 | mean_lateral_swing_m | 0.2833 | 0.2576 | 9.0620 |
| cable_m050_l050 | mean_cable_angle_deg | 34.7595 | 31.1943 | 10.2568 |
| cable_m050_l150 | mean_3d_error_m | 0.4334 | 0.3497 | 19.3211 |
| cable_m050_l150 | rms_3d_error_m | 0.4635 | 0.3657 | 21.0946 |
| cable_m050_l150 | mean_lateral_swing_m | 0.8436 | 0.7668 | 9.0995 |
| cable_m050_l150 | mean_cable_angle_deg | 34.3972 | 30.8706 | 10.2525 |
| mass_m100_l100 | mean_3d_error_m | 0.4915 | 0.4691 | 4.5475 |
| mass_m100_l100 | rms_3d_error_m | 0.5236 | 0.4863 | 7.1364 |
| mass_m100_l100 | mean_lateral_swing_m | 0.5648 | 0.5087 | 9.9282 |
| mass_m100_l100 | mean_cable_angle_deg | 34.6221 | 30.7442 | 11.2005 |
| mass_m200_l100 | mean_3d_error_m | 0.5908 | 0.7424 | -25.6555 |
| mass_m200_l100 | rms_3d_error_m | 0.6266 | 0.7626 | -21.7118 |
| mass_m200_l100 | mean_lateral_swing_m | 0.5633 | 0.4937 | 12.3591 |
| mass_m200_l100 | mean_cable_angle_deg | 34.4996 | 29.7272 | 13.8331 |
| nominal_m050_l100 | mean_3d_error_m | 0.4458 | 0.3358 | 24.6684 |
| nominal_m050_l100 | rms_3d_error_m | 0.4755 | 0.3504 | 26.3060 |
| nominal_m050_l100 | mean_lateral_swing_m | 0.5631 | 0.5144 | 8.6541 |
| nominal_m050_l100 | mean_cable_angle_deg | 34.5050 | 31.1301 | 9.7808 |

## Plots

- `payload_parameter_tracking_error.png`
- `payload_parameter_swing.png`
- `payload_parameter_improvement.png`

## Interpretation

This is a screening dataset, not the final payload robustness campaign. It is meant to identify which payload changes are safe for larger repeatability batches and which cases expose controller limits. All valid cases are retained in the comparison.

The main finding is that the tuned geometric controller remains robust to cable-length changes at the nominal `0.05 kg` payload mass. For both the `0.5 m` and `1.5 m` cable cases, it improves tracking error by roughly `19-21%` and reduces mean cable angle by roughly `10%`.

Payload mass is more sensitive. With a `0.10 kg` payload, the geometric controller still improves swing by `9.93%` and cable angle by `11.20%`, but tracking improvement drops to `4.55%`. With a `0.20 kg` payload, the geometric controller reduces swing by `12.36%` and cable angle by `13.83%`, but tracking error becomes worse than the PX4 baseline by `25.66%`.

This indicates a clear controller tradeoff: the current tuning suppresses swing across all tested payload cases, but heavier payloads need mass-aware thrust/attitude tuning to avoid trajectory-tracking degradation.
