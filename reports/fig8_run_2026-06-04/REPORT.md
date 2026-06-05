# Figure-8 SITL Verification Report

Date: 2026-06-04

## What Was Verified

- Built `px4_sitl_default` successfully.
- Started `MicroXRCEAgent udp4 -p 8888`.
- Launched PX4 SITL with Gazebo Classic `iris_depth_camera` in headless mode.
- Confirmed Gazebo camera streams:
  - `/camera/image_raw`
  - `/camera/depth/image_raw`
  - `/camera/points`
- Confirmed PX4 ROS 2 bridge topics under `/fmu/in/*` and `/fmu/out/*`.
- Ran `figure8_offboard.py`.
- PX4 accepted the external command, armed, and detected takeoff.
- Logged a 24.19 s local-position trace with 1,210 samples.
- Generated trajectory plots from the ROS 2 local-position trace.
- Performed a short Gazebo GUI launch pass; PX4 reported the vehicle ready for takeoff.

## Evidence

- Local position CSV: `local_position_trace.csv`
- X-Y plot: `figure8_xy.png`
- X/Y/Z versus time plot: `figure8_xyz_vs_time.png`
- 3D trajectory plot: `figure8_3d.png`
- Desktop screenshot from GUI pass: `gazebo_gui_screenshot.png`
- PX4 ULog: `build/px4_sitl_default/rootfs/log/2026-06-04/18_03_06.ulg`

## Run Summary

- X range: -6.11 m to 6.10 m
- Y range: -4.16 m to 4.07 m
- Z range: -5.01 m to -4.90 m
- Pointcloud stream observed at roughly 4-8 Hz during the run.
- Note: `gazebo_gui_screenshot.png` captured the active desktop/VS Code rather than the Gazebo viewport, likely because the Gazebo client was behind another window or on another workspace. The verified visual evidence for the run is therefore the generated trajectory plots.

## Project Status

Completed:

- SITL build works on this machine.
- PX4 <-> MicroXRCEAgent <-> ROS 2 bridge works.
- Depth camera and pointcloud topics are visible in ROS 2.
- Offboard Figure-8 position/velocity command node is functional.
- Vehicle can arm, take off, and follow a continuous Figure-8 path.
- ULog and ROS 2 trajectory evidence can be produced.

Remaining:

- Move `figure8_offboard.py` into a proper ROS 2 package instead of keeping it as a root-level script.
- Add a clean launch file that starts MicroXRCEAgent, PX4 SITL, Gazebo, and the offboard node reproducibly.
- Add automatic trajectory logging/plot generation as part of the run workflow.
- Recreate or verify the x500-specific model path if the professor expects x500 screenshots rather than the currently runnable `iris_depth_camera` Gazebo Classic baseline.
- Reintegrate/verify the slung-payload SDF changes; this checkout does not currently show a committed custom payload model.
- Add payload swing metrics: cable angle, payload displacement, and UAV-payload separation versus time.
- Add path-tracking metrics: reference vs actual trajectory, RMS position error, max error, and settling behavior.
- Optional next controller step: implement the geometric controller reference from the paper for attitude/thrust-level tracking instead of only position/velocity setpoints.
