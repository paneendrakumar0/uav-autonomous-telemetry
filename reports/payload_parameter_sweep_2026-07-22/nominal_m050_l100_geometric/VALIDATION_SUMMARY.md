# Single Validation Run

**Created**: 2026-07-22T19:33:36
**Profile**: `geometric`
**Launch File**: `geometric_figure8_experiment.launch.py`
**Flight Duration**: `75.0 s`
**Omega**: `0.25`
**Hover Thrust**: `0.72`

## Result

- Tracking valid: `True`
- Tracking reason: valid tracking telemetry
- Payload swing reason: valid payload swing telemetry

## Metrics

- `samples`: `3722`
- `duration_s`: `74.4280`
- `mean_3d_error_m`: `0.3358`
- `rms_3d_error_m`: `0.3504`
- `max_3d_error_m`: `0.5686`
- `mean_xy_error_m`: `0.3356`
- `mean_z_ned_m`: `-4.9951`
- `max_abs_position_m`: `5.0197`
- `mean_altitude_error_m`: `0.0049`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18581`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0011`
- `mean_lateral_swing_m`: `0.5144`
- `max_lateral_swing_m`: `0.6730`
- `mean_cable_angle_deg`: `31.1301`
- `max_cable_angle_deg`: `42.2015`
- `profile`: `geometric`
- `launch_file`: `geometric_figure8_experiment.launch.py`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `/home/paneendra/uav-autonomous-telemetry/reports/payload_parameter_sweep_2026-07-22/nominal_m050_l100_geometric`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
