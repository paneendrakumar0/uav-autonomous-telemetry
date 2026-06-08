# Corrected Attitude Topic, hover_thrust=0.62 - 2026-06-08

## Objective

Validate the geometric attitude/thrust Figure-8 prototype on the no-payload `iris_depth_camera` target after fixing the PX4 DDS attitude-setpoint topic.

## Setup

- Vehicle: `iris_depth_camera`
- Controller: `geometric_figure8_attitude`
- Attitude topic: `/fmu/in/vehicle_attitude_setpoint_v1`
- Figure-8 amplitude: `5.0 m`
- Angular rate: `0.20 rad/s`
- Target altitude: `-5.0 m` NED
- Hover thrust parameter: `0.62`

## Result

PX4 received fresh `vehicle_attitude_setpoint` updates, accepted Offboard/arm commands, detected takeoff, and flew the slow no-payload Figure-8 commissioning run.

## Metrics

- Samples: `3731`
- Duration: `74.61 s`
- Minimum actual Z NED: `-4.397 m`
- Maximum actual Z NED: `-0.029 m`
- Final actual Z NED: `-4.372 m`
- Post-20s mean 3D error: `0.683 m`
- Post-20s RMS 3D error: `0.683 m`
- Post-20s maximum 3D error: `0.760 m`
- Post-20s mean altitude: `-4.361 m` NED

## Interpretation

This validates the ROS 2 to PX4 attitude/thrust transport path. The tuned `hover_thrust=0.70` run is the preferred no-payload commissioning baseline for the next slung-payload attitude-control test.

## Artifacts

- `geometric_figure8_tracking_metrics.csv`
- `geometric_attitude_v1_altitude_error.png`
- `geometric_attitude_v1_3d.png`
