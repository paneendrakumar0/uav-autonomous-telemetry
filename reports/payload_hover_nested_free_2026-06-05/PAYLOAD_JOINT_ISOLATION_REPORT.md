# Payload Joint Isolation Report - 2026-06-05

## Objective
Find why the `iris_depth_payload` model accepted PX4 offboard commands but stayed near ground level during hover validation.

## What Changed
The payload was moved into a separate nested Gazebo model, `slung_payload_ball`, instead of being defined as a top-level link in `iris_depth_payload`. Three isolation cases were tested under the same `iris_depth_payload` PX4 target and the same hover controller.

## Results

| Case | Payload Structure | Joint to Iris | Final Z NED | Post-12s Mean Error | Result |
| --- | --- | --- | ---: | ---: | --- |
| No-payload control | Iris + depth camera only | None | `-4.995 m` | `0.064 m` | Hover succeeds |
| Nested free payload | Nested payload visual/mass model | None | `-5.000 m` | `0.062 m` | Hover succeeds |
| Nested fixed payload | Nested payload model | Fixed joint | `-0.006 m` | `4.980 m` | Hover fails |

## Diagnosis
The `iris_depth_payload` target and ROS 2 offboard controller are healthy. A payload model can be present in the Gazebo scene without breaking hover. The failure appears when a Gazebo Classic joint physically connects the payload to `iris::base_link`; even a fixed joint prevents the vehicle from climbing.

This means the next real slung-payload step should not be more controller tuning. It should be replacing the direct cross-model Gazebo joint with a safer payload coupling method, such as an integrated single-model SDF payload link chain, a dedicated Gazebo plugin that applies cable tension forces, or a validated joint strategy inside a non-nested Iris model.

## Metrics

### Nested Free Payload Hover
- Duration: `65.37 s`
- Samples: `3269`
- Target altitude: `-5.00 m` NED
- Final altitude: `-5.000 m` NED
- Post-12s mean tracking error: `0.062 m`
- Post-12s RMS tracking error: `0.069 m`
- Post-12s mean XY drift: `0.060 m`
- Maximum XY drift: `0.186 m`

## Artifacts
- `nested_free_hover_xyz_vs_time.png`
- `nested_free_hover_xy_drift.png`
- `nested_free_payload_hover_3d.png`
- `payload_isolation_altitude_comparison.png`
- `payload_isolation_error_comparison.png`
- `hover_tracking_metrics.csv`
