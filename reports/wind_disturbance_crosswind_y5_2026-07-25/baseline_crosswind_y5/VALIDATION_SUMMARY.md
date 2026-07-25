# Single Validation Run

**Created**: 2026-07-25T10:52:39
**Profile**: `baseline`
**Launch File**: `figure8_payload_experiment.launch.py`
**World**: `payload_crosswind_y5`
**Flight Duration**: `75.0 s`
**Omega**: `0.25`
**Hover Thrust**: `0.72`

## Result

- Tracking valid: `True`
- Tracking reason: valid tracking telemetry
- Payload swing reason: valid payload swing telemetry

## Metrics

- `samples`: `3706`
- `duration_s`: `74.1001`
- `mean_3d_error_m`: `0.4467`
- `rms_3d_error_m`: `0.4782`
- `max_3d_error_m`: `0.7103`
- `mean_xy_error_m`: `0.4465`
- `mean_z_ned_m`: `-5.0028`
- `max_abs_position_m`: `5.7881`
- `mean_altitude_error_m`: `0.0028`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18544`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0012`
- `mean_lateral_swing_m`: `0.5662`
- `max_lateral_swing_m`: `0.7268`
- `mean_cable_angle_deg`: `34.7045`
- `max_cable_angle_deg`: `46.4981`
- `profile`: `baseline`
- `launch_file`: `figure8_payload_experiment.launch.py`
- `world`: `payload_crosswind_y5`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `reports/wind_disturbance_crosswind_y5_2026-07-25/baseline_crosswind_y5`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
