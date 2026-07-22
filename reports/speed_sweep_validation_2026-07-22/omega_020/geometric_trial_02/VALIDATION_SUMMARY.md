# Single Validation Run

**Created**: 2026-07-22T18:45:19
**Profile**: `geometric`
**Launch File**: `geometric_figure8_experiment.launch.py`
**Flight Duration**: `75.0 s`
**Omega**: `0.2`
**Hover Thrust**: `0.72`

## Result

- Tracking valid: `True`
- Tracking reason: valid tracking telemetry
- Payload swing reason: valid payload swing telemetry

## Metrics

- `samples`: `3708`
- `duration_s`: `74.1476`
- `mean_3d_error_m`: `0.3127`
- `rms_3d_error_m`: `0.3246`
- `max_3d_error_m`: `0.5237`
- `mean_xy_error_m`: `0.3125`
- `mean_z_ned_m`: `-4.9959`
- `max_abs_position_m`: `5.0175`
- `mean_altitude_error_m`: `0.0041`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18540`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0008`
- `mean_lateral_swing_m`: `0.4401`
- `max_lateral_swing_m`: `0.5874`
- `mean_cable_angle_deg`: `26.2128`
- `max_cable_angle_deg`: `35.9157`
- `profile`: `geometric`
- `launch_file`: `geometric_figure8_experiment.launch.py`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `reports/speed_sweep_validation_2026-07-22/omega_020/geometric_trial_02`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
