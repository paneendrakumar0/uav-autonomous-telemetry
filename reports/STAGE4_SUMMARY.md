# Controller Benchmark Summary - 2026-06-08

This benchmark condenses the completed SITL runs into a single controller-performance view. The purpose is to establish a numerical baseline before moving from PX4 position/velocity offboard setpoints toward a geometric controller or payload-aware control law.

## Tracking Performance

| Case | Profile | Samples | Duration (s) | Steady Window | Mean 3D Error (m) | RMS 3D Error (m) | Max 3D Error (m) | Mean XY Error (m) | Mean Z NED (m) | Final Z NED (m) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| No-payload Figure-8 tuned baseline | Figure-8, position+velocity setpoints | 4305 | 86.093 | t >= 12 s | 0.415 | 0.442 | 0.660 | 0.414 | -4.994 | -4.983 |
| Native ball-joint payload hover | Hover, physical payload attached | 3303 | 66.049 | t >= 12 s | 0.061 | 0.069 | 0.129 | 0.059 | -5.002 | -4.995 |
| Native ball-joint payload Figure-8 | Figure-8, physical payload attached | 7545 | 150.913 | t >= 25 s | 0.462 | 0.493 | 0.796 | 0.462 | -4.996 | -4.987 |
| Stage 4: Geometric omega=0.25 | Figure-8, geometric + smooth ramp | 7449 | 148.989 | t >= 25 s | 0.334 | 0.346 | 0.609 | 0.334 | -4.992 | -4.995 |
| Stage 4: Geometric omega=0.20 | Figure-8, geometric + smooth ramp | 7450 | 149.002 | t >= 25 s | 0.297 | 0.308 | 0.480 | 0.296 | -4.991 | -4.990 |
| Stage 4: Geometric omega=0.15 | Figure-8, geometric + smooth ramp | 7472 | 149.442 | t >= 25 s | 0.230 | 0.238 | 0.399 | 0.229 | -4.991 | -4.989 |

## Payload Swing Diagnostics

| Case | Samples | Steady Window | Mean Lateral Swing (m) | Max Lateral Swing (m) | Mean Cable Angle (deg) | Max Cable Angle (deg) | Mean Cable Length (m) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Native ball-joint payload hover | 16455 | t >= 12 s | 1.405 | 1.475 | 57.969 | 60.113 | 1.657 |
| Native ball-joint payload Figure-8 | 37644 | t >= 25 s | 5.180 | 10.541 | 75.601 | 86.271 | 5.271 |
| Stage 4: Geometric omega=0.25 | 37217 | t >= 25 s | 0.515 | 0.673 | 31.188 | 42.236 | 1.001 |
| Stage 4: Geometric omega=0.20 | 37246 | t >= 25 s | 0.431 | 0.599 | 25.667 | 36.744 | 1.001 |
| Stage 4: Geometric omega=0.15 | 37318 | t >= 25 s | 0.343 | 0.487 | 20.107 | 29.088 | 1.000 |

## Interpretation

- The no-payload Figure-8 remains the clean reference case for evaluating controller changes.
- The native ball-joint payload model now climbs, hovers, and completes the requested 8-shaped circuit.
- The payload Figure-8 tracking error is close to the no-payload tuned baseline, which means the current PX4 offboard position/velocity interface is already a valid baseline for Professor Zavoli's requested test.
- The swing logger values are diagnostic rather than final physical truth, because they are reconstructed from Gazebo pose-sniffer packets and frame conventions. The next control milestone should include a tighter payload-state estimator before claiming swing-angle suppression.
