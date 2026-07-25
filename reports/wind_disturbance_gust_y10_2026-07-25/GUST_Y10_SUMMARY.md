# Gust Disturbance Validation - 2026-07-25

## Purpose

This phase tests recovery from a finite-duration gust after the constant-crosswind screening. The goal is to separate steady disturbance rejection from transient shock response.

## Setup

- Vehicle: `iris_depth_payload`
- Payload: nominal `0.05 kg`, `1.0 m` cable
- Trajectory: Figure-8
- Angular rate: `0.25 rad/s`
- Wind world: `payload_gust_y10`
- Wind model: Gazebo Classic `libgazebo_wind_plugin.so`
- Background wind: `0 m/s`
- Gust velocity: `10.0 m/s`
- Gust direction: `0 1 0`, positive Y direction
- Gust window: starts at `35 s`, duration `15 s`
- Controllers: PX4 position/velocity baseline and tuned geometric attitude/thrust controller
- Trials: `1` baseline + `1` geometric screening trial

## Metrics

| Metric | PX4 baseline | Geometric | Geometric improvement |
| --- | ---: | ---: | ---: |
| Mean 3D tracking error | `0.5427 m` | `0.4554 m` | `16.08%` |
| RMS 3D tracking error | `0.6266 m` | `0.6022 m` | `3.90%` |
| Max 3D tracking error | `1.8162 m` | `2.8165 m` | `-55.08%` |
| Mean lateral swing | `0.5646 m` | `0.5275 m` | `6.57%` |
| Max lateral swing | `0.7220 m` | `0.8270 m` | `-14.54%` |
| Mean cable angle | `34.5853 deg` | `32.0458 deg` | `7.34%` |
| Max cable angle | `46.1004 deg` | `55.6216 deg` | `-20.65%` |

## Evidence

- Baseline summary: `baseline_gust_y10/VALIDATION_SUMMARY.md`
- Geometric summary: `geometric_gust_y10/VALIDATION_SUMMARY.md`
- Baseline plots: `baseline_gust_y10/validation_*.png`
- Geometric plots: `geometric_gust_y10/validation_*.png`
- Comparison CSV: `gust_y10_controller_comparison.csv`

## Interpretation

Both controllers completed the Figure-8 circuit and passed validation under the `10 m/s` gust.

Unlike the constant-crosswind result, the geometric controller improves mean tracking error and mean payload swing during the gust experiment. However, it also produces larger peak tracking error and larger peak cable-angle response. This suggests the geometric controller recovers well on average but has a stronger transient overshoot during sudden disturbances.

The next controller-design implication is clear: disturbance-aware tuning should penalize peak excursion and payload-angle overshoot, not only steady-state or mean tracking error.
