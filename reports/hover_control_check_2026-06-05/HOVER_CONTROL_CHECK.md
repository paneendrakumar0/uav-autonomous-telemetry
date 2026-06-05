# Hover Controller Check - 2026-06-05

Model: `gazebo-classic_iris_depth_camera`

The same `hover_offboard` node used in the payload hover test successfully climbed the normal depth-camera Iris model to the commanded `z=-5 m` hover point.

- Samples: 2721
- Duration: 54.40 s
- Final z: -5.010 m NED
- z range: -5.010 to 0.002 m NED
- Full-run mean error: 0.639 m
- Post-12s mean error: 0.067 m

Conclusion: hover/offboard control is valid. The payload hover failure is isolated to the payload Gazebo model/joint setup.

## Generated Plots

- `hover_control_check_z.png`
- `hover_control_check_xy_drift.png`
- `hover_control_check_3d.png`

## Plot Preview

![No-payload hover z response](hover_control_check_z.png)

![No-payload hover XY drift](hover_control_check_xy_drift.png)

![No-payload hover 3D trajectory](hover_control_check_3d.png)
