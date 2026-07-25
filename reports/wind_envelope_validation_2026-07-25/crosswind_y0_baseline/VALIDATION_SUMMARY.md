# Single Validation Run

**Created**: 2026-07-25T11:28:09
**Profile**: `baseline`
**Launch File**: `figure8_payload_experiment.launch.py`
**World**: `payload_crosswind_y0`
**Flight Duration**: `75.0 s`
**Omega**: `0.25`
**Hover Thrust**: `0.72`

## Result

- Tracking valid: `True`
- Tracking reason: valid tracking telemetry
- Payload swing reason: valid payload swing telemetry

## Metrics

- `samples`: `3710`
- `duration_s`: `74.1794`
- `mean_3d_error_m`: `0.4432`
- `rms_3d_error_m`: `0.4735`
- `max_3d_error_m`: `0.6707`
- `mean_xy_error_m`: `0.4428`
- `mean_z_ned_m`: `-4.9989`
- `max_abs_position_m`: `5.3875`
- `mean_altitude_error_m`: `0.0011`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18550`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0012`
- `mean_lateral_swing_m`: `0.5644`
- `max_lateral_swing_m`: `0.7302`
- `mean_cable_angle_deg`: `34.6004`
- `max_cable_angle_deg`: `46.7787`
- `profile`: `baseline`
- `launch_file`: `figure8_payload_experiment.launch.py`
- `world`: `payload_crosswind_y0`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `/home/paneendra/uav-autonomous-telemetry/reports/wind_envelope_validation_2026-07-25/crosswind_y0_baseline`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
