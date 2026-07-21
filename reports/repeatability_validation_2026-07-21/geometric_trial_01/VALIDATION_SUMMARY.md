# Single Validation Run

**Created**: 2026-07-21T20:19:19
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

- `samples`: `3709`
- `duration_s`: `74.1721`
- `mean_3d_error_m`: `0.3409`
- `rms_3d_error_m`: `0.3558`
- `max_3d_error_m`: `0.5802`
- `mean_xy_error_m`: `0.3407`
- `mean_z_ned_m`: `-4.9946`
- `max_abs_position_m`: `5.0181`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18539`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0010`
- `mean_lateral_swing_m`: `0.5146`
- `max_lateral_swing_m`: `0.6737`
- `mean_cable_angle_deg`: `31.1483`
- `max_cable_angle_deg`: `42.2587`
- `profile`: `geometric`
- `launch_file`: `geometric_figure8_experiment.launch.py`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `reports/repeatability_validation_2026-07-21/geometric_trial_01`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
