# Single Validation Run

**Created**: 2026-07-25T11:40:55
**Profile**: `geometric`
**Launch File**: `geometric_figure8_experiment.launch.py`
**World**: `payload_crosswind_y10`
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
- `mean_3d_error_m`: `2.5982`
- `rms_3d_error_m`: `2.6141`
- `max_3d_error_m`: `3.0526`
- `mean_xy_error_m`: `2.5969`
- `mean_z_ned_m`: `-5.0802`
- `max_abs_position_m`: `7.4518`
- `mean_altitude_error_m`: `0.0802`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18542`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0010`
- `mean_lateral_swing_m`: `0.5139`
- `max_lateral_swing_m`: `0.6727`
- `mean_cable_angle_deg`: `31.0984`
- `max_cable_angle_deg`: `42.1820`
- `profile`: `geometric`
- `launch_file`: `geometric_figure8_experiment.launch.py`
- `world`: `payload_crosswind_y10`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `/home/paneendra/uav-autonomous-telemetry/reports/wind_envelope_validation_2026-07-25/crosswind_y10_geometric`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
