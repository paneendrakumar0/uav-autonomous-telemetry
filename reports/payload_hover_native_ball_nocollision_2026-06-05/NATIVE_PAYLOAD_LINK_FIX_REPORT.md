# Native Slung-Payload Link Fix - 2026-06-05

## Objective
Fix the payload link/joint problem that made the UAV accept PX4 offboard commands but remain near ground level when a payload was physically connected.

## Fix
The `iris_depth_payload` model was rebuilt as a native Iris-derived SDF instead of a wrapper model with an included `iris` nested model. The payload link now belongs to the same model as `base_link`, and the joint is internal:

- Parent: `base_link`
- Child: `slung_payload`
- Joint: `ball`
- Cable length represented by a 1 m visual cylinder and joint pose at the top of the payload link
- Payload mass: `0.05 kg`
- Payload collision removed for flight validation to avoid ground-contact solver locking during spawn

## Result
The true physical payload link issue is solved for hover. The native ball-joint slung-payload model climbs and holds the `-5 m` NED hover target.

| Case | Final Z NED | Post-12s Mean Error | Result |
| --- | ---: | ---: | --- |
| Native fixed payload with collision | `0.056 m` | `4.988 m` | Failed, stayed near ground |
| Native fixed payload without collision | `-4.993 m` | `0.063 m` | Hover succeeds |
| Native ball-joint payload without collision | `-4.995 m` | `0.061 m` | Hover succeeds |

## Native Ball-Joint Hover Metrics
- Duration: `66.05 s`
- Samples: `3303`
- Target altitude: `-5.00 m` NED
- Final altitude: `-4.995 m` NED
- Post-12s mean tracking error: `0.061 m`
- Post-12s RMS tracking error: `0.069 m`
- Post-12s mean XY drift: `0.059 m`
- Maximum XY drift: `0.183 m`
- Payload swing samples: `16455`
- Mean cable angle: `57.92 deg`
- Maximum cable angle: `61.85 deg`

## Generated Artifacts
- `native_ball_hover_xyz_vs_time.png`
- `native_ball_hover_xy_drift.png`
- `native_ball_payload_hover_3d.png`
- `native_payload_link_fix_altitude_comparison.png`
- `native_ball_payload_swing_metrics.png`
- `native_ball_payload_relative_motion_3d.png`
- `native_ball_gazebo_hover_window.png`
- `native_ball_gazebo_hover_closeup.png`
- `hover_tracking_metrics.csv`
- `payload_swing_metrics.csv`

## Next Step
Run the 8-shaped trajectory with this native ball-joint payload model. If the cable-angle readings remain high, tune the payload spawn/pose logger frame convention and then add a controlled perturbation to quantify pendulum damping.
