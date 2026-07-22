# Single Validation Run

**Created**: 2026-07-22T18:36:12
**Profile**: `geometric`
**Launch File**: `geometric_figure8_experiment.launch.py`
**Flight Duration**: `75.0 s`
**Omega**: `0.15`
**Hover Thrust**: `0.72`

## Result

- Tracking valid: `True`
- Tracking reason: valid tracking telemetry
- Payload swing reason: valid payload swing telemetry

## Metrics

- `samples`: `3704`
- `duration_s`: `74.0603`
- `mean_3d_error_m`: `0.2206`
- `rms_3d_error_m`: `0.2295`
- `max_3d_error_m`: `0.3498`
- `mean_xy_error_m`: `0.2203`
- `mean_z_ned_m`: `-4.9933`
- `max_abs_position_m`: `5.0552`
- `mean_altitude_error_m`: `0.0067`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18521`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0005`
- `mean_lateral_swing_m`: `0.3555`
- `max_lateral_swing_m`: `0.4910`
- `mean_cable_angle_deg`: `20.8925`
- `max_cable_angle_deg`: `29.3774`
- `profile`: `geometric`
- `launch_file`: `geometric_figure8_experiment.launch.py`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `reports/speed_sweep_validation_2026-07-22/omega_015/geometric_trial_03`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
