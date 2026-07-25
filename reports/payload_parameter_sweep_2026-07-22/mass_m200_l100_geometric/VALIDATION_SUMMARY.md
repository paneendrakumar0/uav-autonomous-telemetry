# Single Validation Run

**Created**: 2026-07-25T10:29:29
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

- `samples`: `3708`
- `duration_s`: `74.1403`
- `mean_3d_error_m`: `0.7424`
- `rms_3d_error_m`: `0.7626`
- `max_3d_error_m`: `1.1217`
- `mean_xy_error_m`: `0.7034`
- `mean_z_ned_m`: `-4.7701`
- `max_abs_position_m`: `4.8678`
- `mean_altitude_error_m`: `0.2299`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18542`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0010`
- `mean_lateral_swing_m`: `0.4937`
- `max_lateral_swing_m`: `0.6503`
- `mean_cable_angle_deg`: `29.7272`
- `max_cable_angle_deg`: `40.4783`
- `profile`: `geometric`
- `launch_file`: `geometric_figure8_experiment.launch.py`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `/home/paneendra/uav-autonomous-telemetry/reports/payload_parameter_sweep_2026-07-22/mass_m200_l100_geometric`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
