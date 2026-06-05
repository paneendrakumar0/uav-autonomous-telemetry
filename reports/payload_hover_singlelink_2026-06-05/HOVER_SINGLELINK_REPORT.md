# Payload Hover Single-Link Validation - 2026-06-05

## Objective
Validate the next-stage slung-payload hover case after simplifying the payload SDF from a two-joint cable/body model to a single ball-joint pendulum model. The target hover command was `(x, y, z_NED) = (0, 0, -5 m)`.

## Result
PX4 accepted offboard control, armed successfully, and reported takeoff detection. However, the vehicle did not climb in the Gazebo payload configuration. The same hover controller was previously validated on the non-payload depth-camera Iris model, so this run isolates the remaining blocker to the payload model/joint physics rather than the ROS 2 offboard control path.

## Tracking Summary
- Duration: 107.36 s
- Samples: 5368
- Target altitude: -5.00 m NED
- Final altitude: 0.028 m NED
- Post-12 s mean tracking error: 5.008 m
- Post-12 s RMS tracking error: 5.009 m
- Maximum tracking error: 5.059 m
- Post-12 s mean XY drift: 0.035 m
- Maximum XY drift: 0.090 m

## Payload Geometry Observation
The payload logger confirms the slung-payload link is present and publishing Gazebo poses. The measured cable angle remains very high because the UAV does not lift away from the spawn configuration, which supports the diagnosis that the current SDF joint/frame setup is still invalid for flight testing.

## Generated Artifacts
- `hover_xyz_vs_time.png`
- `hover_tracking_error.png`
- `hover_xy_drift.png`
- `payload_hover_3d.png`
- `payload_swing_metrics.png`
- `payload_relative_motion_3d.png`
- `hover_tracking_metrics.csv`
- `payload_swing_metrics.csv`

## Recommended Next Action
Use the simplified payload SDF as a debugging baseline, then replace the Gazebo-classic ball-joint payload attachment with a validated fixed/revolute joint chain or a dedicated payload plugin. Re-run the hover case before returning to the 8-shaped circuit with payload attached.
