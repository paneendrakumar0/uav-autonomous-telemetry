# Single Validation Run

**Created**: 2026-07-25T11:00:21
**Profile**: `geometric`
**Launch File**: `geometric_figure8_experiment.launch.py`
**World**: `payload_gust_y10`
**Flight Duration**: `75.0 s`
**Omega**: `0.25`
**Hover Thrust**: `0.72`

## Result

- Tracking valid: `True`
- Tracking reason: valid tracking telemetry
- Payload swing reason: valid payload swing telemetry

## Metrics

- `samples`: `3708`
- `duration_s`: `74.1482`
- `mean_3d_error_m`: `0.4554`
- `rms_3d_error_m`: `0.6022`
- `max_3d_error_m`: `2.8165`
- `mean_xy_error_m`: `0.4553`
- `mean_z_ned_m`: `-4.9978`
- `max_abs_position_m`: `7.8884`
- `mean_altitude_error_m`: `0.0022`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18539`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0011`
- `mean_lateral_swing_m`: `0.5275`
- `max_lateral_swing_m`: `0.8270`
- `mean_cable_angle_deg`: `32.0458`
- `max_cable_angle_deg`: `55.6216`
- `profile`: `geometric`
- `launch_file`: `geometric_figure8_experiment.launch.py`
- `world`: `payload_gust_y10`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `reports/wind_disturbance_gust_y10_2026-07-25/geometric_gust_y10`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
