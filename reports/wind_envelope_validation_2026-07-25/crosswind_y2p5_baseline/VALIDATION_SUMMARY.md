# Single Validation Run

**Created**: 2026-07-25T11:31:48
**Profile**: `baseline`
**Launch File**: `figure8_payload_experiment.launch.py`
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
- `duration_s`: `74.1479`
- `mean_3d_error_m`: `0.4438`
- `rms_3d_error_m`: `0.4739`
- `max_3d_error_m`: `0.6711`
- `mean_xy_error_m`: `0.4436`
- `mean_z_ned_m`: `-5.0029`
- `max_abs_position_m`: `5.3702`
- `mean_altitude_error_m`: `0.0029`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18542`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0012`
- `mean_lateral_swing_m`: `0.5641`
- `max_lateral_swing_m`: `0.7289`
- `mean_cable_angle_deg`: `34.5743`
- `max_cable_angle_deg`: `46.6739`
- `profile`: `baseline`
- `launch_file`: `figure8_payload_experiment.launch.py`
- `world`: `payload_crosswind_y2p5`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `/home/paneendra/uav-autonomous-telemetry/reports/wind_envelope_validation_2026-07-25/crosswind_y2p5_baseline`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
