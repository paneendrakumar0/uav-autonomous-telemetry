# Single Validation Run

**Created**: 2026-07-25T11:37:16
**Profile**: `geometric`
**Launch File**: `geometric_figure8_experiment.launch.py`
**World**: `payload_crosswind_y7p5`
**Flight Duration**: `75.0 s`
**Omega**: `0.25`
**Hover Thrust**: `0.72`

## Result

- Tracking valid: `True`
- Tracking reason: valid tracking telemetry
- Payload swing reason: valid payload swing telemetry

## Metrics

- `samples`: `3705`
- `duration_s`: `74.0846`
- `mean_3d_error_m`: `1.9210`
- `rms_3d_error_m`: `1.9408`
- `max_3d_error_m`: `2.3604`
- `mean_xy_error_m`: `1.9204`
- `mean_z_ned_m`: `-5.0462`
- `max_abs_position_m`: `6.7820`
- `mean_altitude_error_m`: `0.0462`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18540`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0010`
- `mean_lateral_swing_m`: `0.5145`
- `max_lateral_swing_m`: `0.6720`
- `mean_cable_angle_deg`: `31.1359`
- `max_cable_angle_deg`: `42.1293`
- `profile`: `geometric`
- `launch_file`: `geometric_figure8_experiment.launch.py`
- `world`: `payload_crosswind_y7p5`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `/home/paneendra/uav-autonomous-telemetry/reports/wind_envelope_validation_2026-07-25/crosswind_y7p5_geometric`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
