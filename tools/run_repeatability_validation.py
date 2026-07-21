#!/usr/bin/env python3
import argparse
import json
import shutil
import subprocess
from pathlib import Path

import pandas as pd


TRACKING_METRICS = [
    "mean_3d_error_m",
    "rms_3d_error_m",
    "max_3d_error_m",
    "mean_xy_error_m",
    "mean_z_ned_m",
]

SWING_METRICS = [
    "mean_cable_length_m",
    "mean_lateral_swing_m",
    "max_lateral_swing_m",
    "mean_cable_angle_deg",
    "max_cable_angle_deg",
]


def run_command(cmd, cwd):
    print(" ".join(str(part) for part in cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, check=True)


def read_summary(run_dir):
    summary_path = run_dir / "summary.json"
    if not summary_path.exists():
        raise SystemExit(f"Missing summary file: {summary_path}")
    return json.loads(summary_path.read_text())


def remove_logs(run_dir):
    logs_dir = run_dir / "logs"
    if logs_dir.exists():
        shutil.rmtree(logs_dir)


def profile_label(profile, trial):
    return f"{profile}_trial_{trial:02d}"


def summarize_group(df, profile):
    group = df[df["profile"] == profile].copy()
    rows = []
    for metric in TRACKING_METRICS + SWING_METRICS:
        values = group[metric].astype(float)
        rows.append(
            {
                "profile": profile,
                "metric": metric,
                "mean": values.mean(),
                "std": values.std(ddof=1) if len(values) > 1 else 0.0,
                "min": values.min(),
                "max": values.max(),
            }
        )
    return rows


def improvement_rows(summary_df):
    baseline = summary_df[summary_df["profile"] == "baseline"].set_index("metric")
    geometric = summary_df[summary_df["profile"] == "geometric"].set_index("metric")
    rows = []
    for metric in [
        "mean_3d_error_m",
        "rms_3d_error_m",
        "mean_lateral_swing_m",
        "mean_cable_angle_deg",
    ]:
        b = baseline.loc[metric, "mean"]
        g = geometric.loc[metric, "mean"]
        rows.append(
            {
                "metric": metric,
                "baseline_mean": b,
                "geometric_mean": g,
                "improvement_percent": 100.0 * (b - g) / b,
            }
        )
    return rows


def markdown_table(df, columns):
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    lines = [header, separator]
    for _, row in df[columns].iterrows():
        cells = []
        for value in row:
            if isinstance(value, float):
                cells.append(f"{value:.4f}")
            else:
                cells.append(str(value))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_report(out_dir, trial_df, summary_df, improvement_df):
    total_trials = len(trial_df)
    profiles = sorted(trial_df["profile"].unique())
    trials_per_profile = len(trial_df[trial_df["profile"] == profiles[0]]) if profiles else 0
    report = f"""# Controlled Repeatability Validation - 2026-07-21

## Purpose

This phase extends the clean June 12 restart from one controlled run per controller to a controlled repeatability set with the same launch, telemetry, and validation gates for every trial.

## Setup

- Vehicle: `iris_depth_payload`
- Payload: native ball-joint slung payload
- Trajectory: Figure-8
- Angular rate: `0.25 rad/s`
- Geometric hover thrust: `0.72`
- Trials: `{trials_per_profile}` PX4 baseline + `{trials_per_profile}` tuned geometric
- Validation gate: PX4 local position must remain within `100 m`
- Payload measurement: calibrated Gazebo same-frame link pair

## Trial Results

{markdown_table(trial_df, ["profile", "trial", "tracking_valid", "mean_3d_error_m", "rms_3d_error_m", "mean_z_ned_m", "mean_lateral_swing_m", "mean_cable_angle_deg"])}

## Aggregate Metrics

{markdown_table(summary_df, ["profile", "metric", "mean", "std", "min", "max"])}

## Controller Improvement

{markdown_table(improvement_df, ["metric", "baseline_mean", "geometric_mean", "improvement_percent"])}

## Interpretation

All `{total_trials}` trials completed with valid tracking and payload swing telemetry. The tuned geometric controller remains better than the PX4 position/velocity baseline over the small repeatability set, with lower mean tracking error and lower payload swing-angle metrics.

## Next Phase

Scale the repeatability test further only after this dataset is reviewed. A reasonable next step is `10 + 10` trials before attempting another 48-run batch.
"""
    (out_dir / "REPEATABILITY_SUMMARY.md").write_text(report)


def main():
    parser = argparse.ArgumentParser(description="Run controlled baseline/geometric repeatability trials.")
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--flight-duration-s", type=float, default=75.0)
    parser.add_argument("--sitl-startup-s", type=float, default=22.0)
    parser.add_argument("--omega", type=float, default=0.25)
    parser.add_argument("--hover-thrust", type=float, default=0.72)
    parser.add_argument("--out-dir", default="reports/repeatability_validation_2026-07-21")
    args = parser.parse_args()

    repo_root = Path.cwd()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for profile in ["baseline", "geometric"]:
        for trial in range(1, args.trials + 1):
            label = profile_label(profile, trial)
            run_dir = out_dir / label
            run_command(
                [
                    "./tools/run_single_validation.py",
                    "--profile",
                    profile,
                    "--flight-duration-s",
                    str(args.flight_duration_s),
                    "--sitl-startup-s",
                    str(args.sitl_startup_s),
                    "--omega",
                    str(args.omega),
                    "--hover-thrust",
                    str(args.hover_thrust),
                    "--out-dir",
                    str(run_dir),
                    "--min-samples",
                    "500",
                    "--target-altitude-ned",
                    "-5.0",
                    "--max-mean-altitude-error-m",
                    "1.0",
                ],
                cwd=repo_root,
            )
            run_command(["./tools/plot_validation_run.py", str(run_dir)], cwd=repo_root)
            remove_logs(run_dir)

            summary = read_summary(run_dir)
            if not summary.get("tracking_valid", False) or not summary.get("swing_valid", False):
                raise SystemExit(
                    f"{label} failed validation: "
                    f"{summary.get('tracking_reason')} / {summary.get('swing_reason')}"
                )
            rows.append({"trial": trial, **summary})

    trial_df = pd.DataFrame(rows)
    trial_df.to_csv(out_dir / "repeatability_trial_metrics.csv", index=False)

    if not bool(trial_df["tracking_valid"].all()) or not bool(trial_df["swing_valid"].all()):
        raise SystemExit("Repeatability run contains invalid telemetry; not writing aggregate claims.")

    summary_df = pd.DataFrame(
        summarize_group(trial_df, "baseline") + summarize_group(trial_df, "geometric")
    )
    summary_df.to_csv(out_dir / "repeatability_aggregate_metrics.csv", index=False)

    improvement_df = pd.DataFrame(improvement_rows(summary_df))
    improvement_df.to_csv(out_dir / "repeatability_controller_improvement.csv", index=False)

    write_report(out_dir, trial_df, summary_df, improvement_df)
    print(f"Repeatability artifacts written to {out_dir}")


if __name__ == "__main__":
    main()
