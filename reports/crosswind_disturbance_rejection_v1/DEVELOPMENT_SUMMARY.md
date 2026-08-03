# Crosswind Disturbance-Rejection V1 Development Summary

**Date:** 2026-08-02  
**Development winds:** 0, 2.5, and 7.5 m/s  
**Frozen candidate:** `ki_xy=0.35`, `kd_xy=1.3`, integral limit `5.0 m s`, leak rate `0.02 Hz`, maximum tilt `35 deg`

## Design

The candidate adds a leaky, norm-bounded position-error integrator to the geometric attitude/thrust controller. Integration begins only after PX4 confirms armed/offboard state and the takeoff ramp completes. Integration pauses when the previous command saturated, while the stored state continues to leak toward zero. Lateral acceleration is constrained by an explicit tilt limit.

## Bounded Gain Search

The development search was intentionally limited:

- `ki_xy`: 0.25, 0.35, 0.45
- `kd_xy`: 1.1, 1.3, 1.5
- Maximum tilt: 35 and 45 deg

Rejected runs and negative outcomes were retained in the isolated validation workspace. No 5 or 10 m/s candidate flights were used for tuning.

## Selected-Candidate Results

| Wind | PX4 baseline error | Old geometric error | Candidate error | Reduction vs old geometric | PX4 cable angle | Candidate cable angle | Cable-angle improvement |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 m/s | 0.4512 m | 0.4851 m | 0.4864 m | -0.3% | 34.70 deg | 32.19 deg | 7.2% |
| 2.5 m/s | 0.5433 m | 0.7363 m | 0.4320 m | 41.3% | 34.69 deg | 32.91 deg | 5.1% |
| 7.5 m/s | 0.5583 m | 1.9856 m | 0.7730 m | 61.1% | 35.52 deg | 32.08 deg | 9.7% |

## Decision

The candidate is frozen for randomized evaluation because it removes most steady crosswind bias, preserves nominal tracking, beats PX4 baseline tracking at 2.5 m/s, and retains a payload-angle advantage in every development condition.

It does not fully satisfy the aspirational 7% cable-angle floor at 2.5 m/s, and it remains worse than PX4 tracking at 7.5 m/s. The final evaluation must therefore be interpreted as an honest candidate assessment, not confirmation of success.

## Frozen Evaluation Protocol

- Winds: 0, 5, and 10 m/s
- Controllers: PX4 baseline and frozen geometric candidate
- Trials: 5 per controller per wind
- Total flights: 30
- Deterministic randomized order
- Primary outcome: mean 3D tracking error
- Secondary outcomes: RMS/peak tracking error, lateral swing, and cable angle
- No tuning after evaluation begins
