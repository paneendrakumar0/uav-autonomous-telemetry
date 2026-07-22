# Single Validation Run

**Created**: 2026-07-22T17:59:26
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

- `samples`: `3723`
- `duration_s`: `74.4438`
- `mean_3d_error_m`: `0.3360`
- `rms_3d_error_m`: `0.3519`
- `max_3d_error_m`: `0.5870`
- `mean_xy_error_m`: `0.3358`
- `mean_z_ned_m`: `-4.9942`
- `max_abs_position_m`: `5.0182`
- `mean_altitude_error_m`: `0.0058`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18544`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0010`
- `mean_lateral_swing_m`: `0.5145`
- `max_lateral_swing_m`: `0.6751`
- `mean_cable_angle_deg`: `31.1405`
- `max_cable_angle_deg`: `42.3696`
- `profile`: `geometric`
- `launch_file`: `geometric_figure8_experiment.launch.py`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `reports/repeatability_validation_10x10_2026-07-22/geometric_trial_01`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
