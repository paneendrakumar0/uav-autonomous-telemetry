# Single Validation Run

**Created**: 2026-07-25T10:58:22
**Profile**: `baseline`
**Launch File**: `figure8_payload_experiment.launch.py`
**World**: `payload_gust_y10`
**Flight Duration**: `75.0 s`
**Omega**: `0.25`
**Hover Thrust**: `0.72`

## Result

- Tracking valid: `True`
- Tracking reason: valid tracking telemetry
- Payload swing reason: valid payload swing telemetry

## Metrics

- `samples`: `3709`
- `duration_s`: `74.1642`
- `mean_3d_error_m`: `0.5427`
- `rms_3d_error_m`: `0.6266`
- `max_3d_error_m`: `1.8162`
- `mean_xy_error_m`: `0.5425`
- `mean_z_ned_m`: `-4.9967`
- `max_abs_position_m`: `5.3495`
- `mean_altitude_error_m`: `0.0033`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18546`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0012`
- `mean_lateral_swing_m`: `0.5646`
- `max_lateral_swing_m`: `0.7220`
- `mean_cable_angle_deg`: `34.5853`
- `max_cable_angle_deg`: `46.1004`
- `profile`: `baseline`
- `launch_file`: `figure8_payload_experiment.launch.py`
- `world`: `payload_gust_y10`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `reports/wind_disturbance_gust_y10_2026-07-25/baseline_gust_y10`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
