# Single Validation Run

**Created**: 2026-07-25T10:54:37
**Profile**: `geometric`
**Launch File**: `geometric_figure8_experiment.launch.py`
**World**: `payload_crosswind_y5`
**Flight Duration**: `75.0 s`
**Omega**: `0.25`
**Hover Thrust**: `0.72`

## Result

- Tracking valid: `True`
- Tracking reason: valid tracking telemetry
- Payload swing reason: valid payload swing telemetry

## Metrics

- `samples`: `3721`
- `duration_s`: `74.4041`
- `mean_3d_error_m`: `1.2690`
- `rms_3d_error_m`: `1.3013`
- `max_3d_error_m`: `1.7224`
- `mean_xy_error_m`: `1.2688`
- `mean_z_ned_m`: `-5.0199`
- `max_abs_position_m`: `6.1640`
- `mean_altitude_error_m`: `0.0199`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18577`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0010`
- `mean_lateral_swing_m`: `0.5139`
- `max_lateral_swing_m`: `0.6671`
- `mean_cable_angle_deg`: `31.0788`
- `max_cable_angle_deg`: `41.7572`
- `profile`: `geometric`
- `launch_file`: `geometric_figure8_experiment.launch.py`
- `world`: `payload_crosswind_y5`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `reports/wind_disturbance_crosswind_y5_2026-07-25/geometric_crosswind_y5`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
