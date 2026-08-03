# Wind Feed-Forward and Payload-Swing Feedback V1: Development Summary

## Outcome

A bounded acceleration-disturbance observer is selected for frozen evaluation with:

- disturbance observer gain: `1.0`
- disturbance low-pass cutoff: `0.3 Hz`
- horizontal disturbance-estimate limit: `4.0 m/s^2`
- payload swing gains: `kp=0.0`, `kd=0.0`
- geometric integral gains: `0.0`
- maximum tilt: `35 deg`

Explicit payload-direction feedback was implemented and verified, but no active swing setting produced a Pareto improvement over the observer-only controller. It therefore remains opt-in and does not advance in this candidate.

## Development Results

All rows below are single-run screening results and are excluded from the official frozen dataset.

| Case | Wind | Mean 3D error (m) | Mean cable angle (deg) | Max cable angle (deg) | Mean observer magnitude (m/s^2) | Mean swing correction (m/s^2) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Zero-gain interface smoke | 0 | 0.3907 | 31.4090 | 41.8278 | 0.0000 | 0.0000 |
| Observer g0.4 / limit1.5 | 5 | 0.8483 | 31.3642 | 41.9236 | 1.4298 | 0.0000 |
| Observer g0.4 / limit1.5 | 0 | 0.2865 | 31.3820 | 46.1804 | 0.5775 | 0.0000 |
| Observer g0.8 / limit1.5 | 5 | 0.4777 | 31.5882 | 42.7542 | 1.4292 | 0.0000 |
| Observer g0.8 / limit1.5 | 10 | 1.8087 | 31.1567 | 43.1294 | 1.5000 | 0.0000 |
| Observer g0.8 / limit3.0 | 10 | 0.9946 | 31.6967 | 43.4510 | 3.0000 | 0.0000 |
| **Observer g1.0 / limit4.0** | **0** | **0.2809** | **32.4981** | **44.7955** | **0.6131** | **0.0000** |
| **Observer g1.0 / limit4.0** | **5** | **0.2481** | **32.2858** | **44.7473** | **1.7708** | **0.0000** |
| **Observer g1.0 / limit4.0** | **10** | **0.3301** | **32.7455** | **44.3875** | **3.6262** | **0.0000** |
| Swing-only kp0.5 / kd0.2 | 5 | 1.2911 | 30.0141 | 41.3983 | 0.0000 | 0.2501 |
| Combined swing kp0.5 / kd0.2 | 5 | 0.2624 | 31.7885 | 48.8744 | 1.7709 | 0.2630 |
| Combined swing kp0.3 / kd0.4 | 5 | 0.2652 | 32.3112 | 44.8312 | 1.8189 | 0.1765 |

The first observer g0.4 wind-5 run preceded controller-telemetry QoS correction. Its flight result was valid but its zero controller-state trace is excluded; the repeated row above is the usable development result.

## Screening Comparison to PX4 Baseline

Using the prior five-trial PX4 baseline means only as a development reference, the selected observer-only candidate reduced mean 3D error by approximately `36.0%`, `45.0%`, and `30.7%` at 0, 5, and 10 m/s. Mean cable angle was approximately `5.5%`, `6.5%`, and `5.2%` lower. These are screening comparisons, not inferential claims.

## Freeze Decision

The observer-only candidate is promising enough for a new randomized evaluation. No further gains may be changed after its first official flight. Success still requires repeated trials and bootstrap intervals; these development runs must not be pooled with the official dataset.
