# Single Validation Run

**Created**: 2026-07-25T11:39:05
**Profile**: `baseline`
**Launch File**: `figure8_payload_experiment.launch.py`
**World**: `payload_crosswind_y10`
**Flight Duration**: `75.0 s`
**Omega**: `0.25`
**Hover Thrust**: `0.72`

## Result

- Tracking valid: `True`
- Tracking reason: valid tracking telemetry
- Payload swing reason: valid payload swing telemetry

## Metrics

- `samples`: `3722`
- `duration_s`: `74.4199`
- `mean_3d_error_m`: `0.4574`
- `rms_3d_error_m`: `0.4871`
- `max_3d_error_m`: `0.6932`
- `mean_xy_error_m`: `0.4572`
- `mean_z_ned_m`: `-5.0078`
- `max_abs_position_m`: `8.7994`
- `mean_altitude_error_m`: `0.0078`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18586`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0012`
- `mean_lateral_swing_m`: `0.5644`
- `max_lateral_swing_m`: `0.7302`
- `mean_cable_angle_deg`: `34.6009`
- `max_cable_angle_deg`: `46.7736`
- `profile`: `baseline`
- `launch_file`: `figure8_payload_experiment.launch.py`
- `world`: `payload_crosswind_y10`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `/home/paneendra/uav-autonomous-telemetry/reports/wind_envelope_validation_2026-07-25/crosswind_y10_baseline`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
