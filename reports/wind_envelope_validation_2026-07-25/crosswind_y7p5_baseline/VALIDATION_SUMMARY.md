# Single Validation Run

**Created**: 2026-07-25T11:35:26
**Profile**: `baseline`
**Launch File**: `figure8_payload_experiment.launch.py`
**World**: `payload_crosswind_y7p5`
**Flight Duration**: `75.0 s`
**Omega**: `0.25`
**Hover Thrust**: `0.72`

## Result

- Tracking valid: `True`
- Tracking reason: valid tracking telemetry
- Payload swing reason: valid payload swing telemetry

## Metrics

- `samples`: `3707`
- `duration_s`: `74.1245`
- `mean_3d_error_m`: `0.4502`
- `rms_3d_error_m`: `0.4808`
- `max_3d_error_m`: `0.6842`
- `mean_xy_error_m`: `0.4499`
- `mean_z_ned_m`: `-5.0079`
- `max_abs_position_m`: `6.8840`
- `mean_altitude_error_m`: `0.0079`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18537`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0012`
- `mean_lateral_swing_m`: `0.5647`
- `max_lateral_swing_m`: `0.7291`
- `mean_cable_angle_deg`: `34.6168`
- `max_cable_angle_deg`: `46.6893`
- `profile`: `baseline`
- `launch_file`: `figure8_payload_experiment.launch.py`
- `world`: `payload_crosswind_y7p5`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `/home/paneendra/uav-autonomous-telemetry/reports/wind_envelope_validation_2026-07-25/crosswind_y7p5_baseline`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
