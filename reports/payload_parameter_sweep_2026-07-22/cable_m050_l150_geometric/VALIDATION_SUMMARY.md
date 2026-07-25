# Single Validation Run

**Created**: 2026-07-25T10:36:59
**Profile**: `geometric`
**Launch File**: `geometric_figure8_experiment.launch.py`
**Flight Duration**: `75.0 s`
**Omega**: `0.25`
**Hover Thrust**: `0.72`

## Result

- Tracking valid: `True`
- Tracking reason: valid tracking telemetry
- Payload swing reason: valid payload swing telemetry

## Metrics

- `samples`: `3723`
- `duration_s`: `74.4442`
- `mean_3d_error_m`: `0.3497`
- `rms_3d_error_m`: `0.3657`
- `max_3d_error_m`: `0.5844`
- `mean_xy_error_m`: `0.3495`
- `mean_z_ned_m`: `-4.9961`
- `max_abs_position_m`: `5.0190`
- `mean_altitude_error_m`: `0.0039`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18586`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.5027`
- `mean_lateral_swing_m`: `0.7668`
- `max_lateral_swing_m`: `0.9994`
- `mean_cable_angle_deg`: `30.8706`
- `max_cable_angle_deg`: `41.6279`
- `profile`: `geometric`
- `launch_file`: `geometric_figure8_experiment.launch.py`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `/home/paneendra/uav-autonomous-telemetry/reports/payload_parameter_sweep_2026-07-22/cable_m050_l150_geometric`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
