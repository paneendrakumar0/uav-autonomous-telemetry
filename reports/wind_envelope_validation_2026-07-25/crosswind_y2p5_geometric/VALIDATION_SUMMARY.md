# Single Validation Run

**Created**: 2026-07-25T11:33:37
**Profile**: `geometric`
**Launch File**: `geometric_figure8_experiment.launch.py`
**World**: `payload_crosswind_y2p5`
**Flight Duration**: `75.0 s`
**Omega**: `0.25`
**Hover Thrust**: `0.72`

## Result

- Tracking valid: `True`
- Tracking reason: valid tracking telemetry
- Payload swing reason: valid payload swing telemetry

## Metrics

- `samples`: `3708`
- `duration_s`: `74.1480`
- `mean_3d_error_m`: `0.6491`
- `rms_3d_error_m`: `0.6945`
- `max_3d_error_m`: `1.0658`
- `mean_xy_error_m`: `0.6490`
- `mean_z_ned_m`: `-5.0007`
- `max_abs_position_m`: `5.4889`
- `mean_altitude_error_m`: `0.0007`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18539`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0010`
- `mean_lateral_swing_m`: `0.5144`
- `max_lateral_swing_m`: `0.6734`
- `mean_cable_angle_deg`: `31.1333`
- `max_cable_angle_deg`: `42.2401`
- `profile`: `geometric`
- `launch_file`: `geometric_figure8_experiment.launch.py`
- `world`: `payload_crosswind_y2p5`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `/home/paneendra/uav-autonomous-telemetry/reports/wind_envelope_validation_2026-07-25/crosswind_y2p5_geometric`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
