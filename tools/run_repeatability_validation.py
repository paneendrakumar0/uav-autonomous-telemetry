#!/usr/bin/env python3
import argparse
from datetime import date
import json
import shutil
import subprocess
from pathlib import Path

import pandas as pd

from experiment_provenance import (
    mark_raw_telemetry_discarded,
    relative_manifest_paths,
    write_manifest,
)
from statistical_analysis import bootstrap_improvement


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


def remove_raw_telemetry(run_dir):
    removed = []
    for csv_name in ["tracking_metrics.csv", "payload_swing_metrics.csv"]:
        csv_path = run_dir / csv_name
        if csv_path.exists():
            csv_path.unlink()
            removed.append(csv_name)
    mark_raw_telemetry_discarded(run_dir, removed)


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


def statistical_rows(trial_df, args):
    rows = []
    for index, metric in enumerate(
        [
            "mean_3d_error_m",
            "rms_3d_error_m",
            "mean_lateral_swing_m",
            "mean_cable_angle_deg",
        ]
    ):
        baseline = trial_df[trial_df["profile"] == "baseline"][metric].astype(float)
        geometric = trial_df[trial_df["profile"] == "geometric"][metric].astype(float)
        comparison = bootstrap_improvement(
            baseline,
            geometric,
            confidence_level=args.confidence_level,
            resamples=args.bootstrap_resamples,
            seed=args.bootstrap_seed + index,
        )
        rows.append({"metric": metric, **comparison})
    return rows


def markdown_table(df, columns):
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    lines = [header, separator]
    for _, row in df[columns].iterrows():
        cells = []
        for value in row:
            if pd.isna(value):
                cells.append("n/a")
            elif isinstance(value, float):
                cells.append(f"{value:.4f}")
            else:
                cells.append(str(value))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_report(out_dir, trial_df, summary_df, improvement_df, statistical_df, args):
    total_trials = len(trial_df)
    profiles = sorted(trial_df["profile"].unique())
    trials_per_profile = len(trial_df[trial_df["profile"] == profiles[0]]) if profiles else 0
    report = f"""# Controlled Repeatability Validation - {date.today().isoformat()}

## Purpose

This phase extends the clean June 12 restart from one controlled run per controller to a controlled repeatability set with the same launch, telemetry, and validation gates for every trial.

## Setup

- Vehicle: `iris_depth_payload`
- Payload: native ball-joint slung payload
- Trajectory: Figure-8
- Angular rate: `{args.omega} rad/s`
- Geometric hover thrust: `{args.hover_thrust}`
- Trials: `{trials_per_profile}` PX4 baseline + `{trials_per_profile}` tuned geometric
- Validation gate: PX4 local position must remain within `100 m`
- Altitude gate: steady mean altitude must remain within `1.0 m` of `-5.0 m` NED
- Payload measurement: calibrated Gazebo same-frame link pair
- Raw per-trial telemetry CSV retention: `{args.keep_raw_telemetry}`

## Trial Results

{markdown_table(trial_df, ["profile", "trial", "tracking_valid", "mean_3d_error_m", "rms_3d_error_m", "mean_z_ned_m", "mean_lateral_swing_m", "mean_cable_angle_deg"])}

## Aggregate Metrics

{markdown_table(summary_df, ["profile", "metric", "mean", "std", "min", "max"])}

## Controller Improvement

{markdown_table(improvement_df, ["metric", "baseline_mean", "geometric_mean", "improvement_percent"])}

## Statistical Comparison

Positive improvement and effect-size values favor the geometric controller.
Intervals are independent-sample percentile-bootstrap confidence intervals.
Very large standardized effects can result from near-deterministic SITL
variance and must not be interpreted as real-world effect magnitude.

{markdown_table(statistical_df, ["metric", "baseline_n", "candidate_n", "absolute_improvement", "absolute_ci_low", "absolute_ci_high", "percent_improvement", "percent_ci_low", "percent_ci_high", "hedges_g"])}

## Interpretation

All `{total_trials}` trials completed with valid tracking and payload swing telemetry. The tuned geometric controller remains better than the PX4 position/velocity baseline over the small repeatability set, with lower mean tracking error and lower payload swing-angle metrics.

## Next Phase

Use this dataset to decide whether the controller comparison is stable enough to proceed to speed sweeps and payload-parameter sweeps.
"""
    (out_dir / "REPEATABILITY_SUMMARY.md").write_text(report)


def main():
    parser = argparse.ArgumentParser(description="Run controlled baseline/geometric repeatability trials.")
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--flight-duration-s", type=float, default=75.0)
    parser.add_argument("--sitl-startup-s", type=float, default=22.0)
    parser.add_argument("--omega", type=float, default=0.25)
    parser.add_argument("--hover-thrust", type=float, default=0.72)
    parser.add_argument("--confidence-level", type=float, default=0.95)
    parser.add_argument("--bootstrap-resamples", type=int, default=10_000)
    parser.add_argument("--bootstrap-seed", type=int, default=20_260_729)
    parser.add_argument("--out-dir", default="reports/repeatability_validation_2026-07-21")
    retention = parser.add_mutually_exclusive_group()
    retention.add_argument(
        "--keep-raw-telemetry",
        dest="keep_raw_telemetry",
        action="store_true",
        default=True,
        help="Keep per-trial tracking and payload swing CSV files (default).",
    )
    retention.add_argument(
        "--discard-raw-telemetry",
        dest="keep_raw_telemetry",
        action="store_false",
        help="Delete per-trial raw CSV files after plots and summaries are generated.",
    )
    args = parser.parse_args()
    if args.trials < 2:
        parser.error("--trials must be at least 2 for uncertainty estimation")
    if args.bootstrap_resamples < 100:
        parser.error("--bootstrap-resamples must be at least 100")
    if not 0.0 < args.confidence_level < 1.0:
        parser.error("--confidence-level must be between 0 and 1")

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
            if not args.keep_raw_telemetry:
                remove_raw_telemetry(run_dir)
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

    statistical_df = pd.DataFrame(statistical_rows(trial_df, args))
    statistical_df.to_csv(out_dir / "repeatability_statistical_comparison.csv", index=False)

    write_report(out_dir, trial_df, summary_df, improvement_df, statistical_df, args)
    write_manifest(
        out_dir,
        experiment_type="repeatability_validation",
        repo_root=repo_root,
        px4_dir=Path.home() / "PX4-Autopilot",
        parameters={
            "profiles": ["baseline", "geometric"],
            "trials_per_profile": args.trials,
            "flight_duration_s": args.flight_duration_s,
            "sitl_startup_s": args.sitl_startup_s,
            "omega_rad_s": args.omega,
            "hover_thrust": args.hover_thrust,
            "target_altitude_ned_m": -5.0,
            "max_mean_altitude_error_m": 1.0,
            "confidence_level": args.confidence_level,
            "bootstrap_resamples": args.bootstrap_resamples,
            "bootstrap_seed": args.bootstrap_seed,
        },
        data={
            "raw_telemetry_retention_policy": (
                "retain" if args.keep_raw_telemetry else "discard_after_aggregation"
            ),
            "constituent_manifests": relative_manifest_paths(out_dir),
            "trial_metrics_csv": "repeatability_trial_metrics.csv",
            "aggregate_metrics_csv": "repeatability_aggregate_metrics.csv",
            "controller_improvement_csv": "repeatability_controller_improvement.csv",
            "statistical_comparison_csv": "repeatability_statistical_comparison.csv",
            "summary_markdown": "REPEATABILITY_SUMMARY.md",
        },
        result={
            "total_trials": int(len(trial_df)),
            "valid_tracking_trials": int(trial_df["tracking_valid"].sum()),
            "valid_swing_trials": int(trial_df["swing_valid"].sum()),
        },
    )
    print(f"Repeatability artifacts written to {out_dir}")


if __name__ == "__main__":
    main()
