# Single Validation Run

**Created**: 2026-07-21T21:33:23
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

- `samples`: `3704`
- `duration_s`: `74.0677`
- `mean_3d_error_m`: `0.3812`
- `rms_3d_error_m`: `0.4181`
- `max_3d_error_m`: `0.7437`
- `mean_xy_error_m`: `0.3809`
- `mean_z_ned_m`: `-4.9937`
- `max_abs_position_m`: `5.1574`
- `mean_altitude_error_m`: `0.0063`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18522`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0010`
- `mean_lateral_swing_m`: `0.5068`
- `max_lateral_swing_m`: `0.6788`
- `mean_cable_angle_deg`: `30.6596`
- `max_cable_angle_deg`: `42.6546`
- `profile`: `geometric`
- `launch_file`: `geometric_figure8_experiment.launch.py`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `reports/repeatability_validation_5x5_2026-07-21/geometric_trial_03`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
