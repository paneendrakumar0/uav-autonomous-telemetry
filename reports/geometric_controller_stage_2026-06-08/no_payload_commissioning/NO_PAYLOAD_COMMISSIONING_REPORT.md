# No-Payload Geometric Commissioning Run - 2026-06-08

## Objective

Run the new `geometric_figure8_attitude` prototype on the known-good no-payload `iris_depth_camera` target before attempting the slung-payload vehicle.

## Setup

- Vehicle: `iris_depth_camera`
- Simulator: Gazebo Classic, headless
- Controller: `geometric_figure8_attitude`
- Reference: Figure-8 with smooth takeoff ramp
- Amplitude: `5.0 m`
- Angular rate: `0.20 rad/s`
- Target altitude: `-5.0 m` NED
- Hover thrust parameter: `0.62`

## Result

The prototype entered Offboard mode and PX4 accepted the external arm command, but the vehicle did not leave the ground. PX4 later disarmed automatically during preflight/ground-idle. This run is therefore recorded as a commissioning failure, not a validated flight result.

## Metrics

- Samples: `4727`
- Duration: `94.54 s`
- Minimum actual Z NED: `-0.051 m`
- Maximum actual Z NED: `0.080 m`
- Final actual Z NED: `0.005 m`
- Post-12s mean 3D error: `6.371 m`
- Post-12s maximum 3D error: `7.110 m`

## Diagnosis

This failure is isolated to the new attitude/thrust prototype, because the same SITL target previously completes Figure-8 tracking with the validated PX4 position/velocity setpoint controller. PX4 reported Offboard as the intended navigation mode after the run, so the next debug step is the attitude/thrust setpoint interface and thrust scaling/arming sequence.

## Follow-Up Change

After this run, the prototype command order was adjusted to request Offboard mode before sending the arm command. The next commissioning run should verify whether attitude thrust is accepted while armed and should inspect `vehicle_attitude_setpoint.thrust_body[2]` during active publication.

## Artifacts

- `geometric_figure8_tracking_metrics.csv`
- `geometric_no_payload_commissioning_altitude_error.png`
- `geometric_no_payload_commissioning_3d.png`
