# Matched-Rate Payload Controller Comparison - 2026-06-08

## Objective

Run the geometric attitude/thrust controller on the slung-payload Figure-8 at the same angular rate as the previous PX4 position/velocity payload baseline: `omega=0.25 rad/s`. This removes the main caveat from the first geometric payload run.

## Setup

- Vehicle: `iris_depth_payload`
- Payload: native internal `base_link -> slung_payload` ball joint
- Trajectory: Figure-8 / lemniscate
- Amplitude: `5.0 m`
- Angular rate: `0.25 rad/s`
- Target altitude: `-5.0 m` NED
- Geometric hover thrust: `0.70`
- Steady-state comparison window: `t >= 25 s`

## Result

The geometric attitude/thrust controller completed the matched-rate slung-payload Figure-8. Compared with the existing PX4 position/velocity payload baseline at the same angular rate, the geometric controller reduced mean 3D tracking error by `20.2%`.

## Matched-Rate Tracking Comparison

| Controller | Omega | Samples | Duration | Mean 3D Error | RMS 3D Error | Max 3D Error | Mean XY Error | Mean Z NED | Final Z NED |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| PX4 position/velocity | `0.25` | `6295` | `150.91 s` | `0.462 m` | `0.493 m` | `0.796 m` | `0.462 m` | `-4.996 m` | `-4.987 m` |
| Geometric attitude/thrust | `0.25` | `4480` | `114.60 s` | `0.369 m` | `0.378 m` | `0.624 m` | `0.343 m` | `-4.867 m` | `-4.857 m` |

## Interpretation

At matched angular rate, the geometric controller improves tracking error while holding slightly lower altitude than the PX4 position/velocity baseline. This is now a fairer controller comparison than the first geometric payload run. The next research step is to repeat both cases over multiple trials and calibrate payload swing estimation.

## Geometric Payload Swing Diagnostics

- Payload samples: `28582`
- Post-25s mean lateral swing: `4.581 m`
- Post-25s maximum lateral swing: `9.252 m`
- Post-25s mean cable angle: `74.637 deg`
- Post-25s maximum cable angle: `85.486 deg`
- Post-25s mean cable length estimate: `4.680 m`

These payload swing values remain diagnostic until the pose-sniffer frame/cable-length convention is calibrated.

## Artifacts

- `geometric_payload_omega025_tracking_metrics.csv`
- `geometric_payload_omega025_swing_metrics.csv`
- `matched_payload_xy_tracking.png`
- `matched_payload_xy_tracking_steady.png`
- `matched_payload_3d_tracking.png`
- `matched_payload_error_altitude.png`
- `matched_geometric_swing_diagnostics.png`
