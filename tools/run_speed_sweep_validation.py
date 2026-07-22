#!/usr/bin/env python3
import argparse
import subprocess
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


IMPROVEMENT_METRICS = [
    "mean_3d_error_m",
    "rms_3d_error_m",
    "mean_lateral_swing_m",
    "mean_cable_angle_deg",
]


def run_command(cmd, cwd):
    print(" ".join(str(part) for part in cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, check=True)


def omega_label(omega):
    return f"omega_{int(round(omega * 100)):03d}"


def read_required_csv(path):
    if not path.exists():
        raise SystemExit(f"Missing required CSV: {path}")
    return pd.read_csv(path)


def collect_speed_rows(out_dir, omega):
    run_dir = out_dir / omega_label(omega)
    aggregate = read_required_csv(run_dir / "repeatability_aggregate_metrics.csv")
    improvement = read_required_csv(run_dir / "repeatability_controller_improvement.csv")

    metric_rows = []
    for _, row in aggregate.iterrows():
        metric_rows.append(
            {
                "omega_rad_s": omega,
                "profile": row["profile"],
                "metric": row["metric"],
                "mean": row["mean"],
                "std": row["std"],
                "min": row["min"],
                "max": row["max"],
            }
        )

    improvement_rows = []
    for _, row in improvement.iterrows():
        improvement_rows.append(
            {
                "omega_rad_s": omega,
                "metric": row["metric"],
                "baseline_mean": row["baseline_mean"],
                "geometric_mean": row["geometric_mean"],
                "improvement_percent": row["improvement_percent"],
            }
        )

    return metric_rows, improvement_rows


def metric_value(profile_metrics, omega, profile, metric):
    match = profile_metrics[
        (profile_metrics["omega_rad_s"] == omega)
        & (profile_metrics["profile"] == profile)
        & (profile_metrics["metric"] == metric)
    ]
    if match.empty:
        raise SystemExit(f"Missing {profile}/{metric} at omega={omega}")
    return float(match.iloc[0]["mean"])


def plot_tracking_and_swing(out_dir, profile_metrics, omegas):
    fig, axes = plt.subplots(2, 1, figsize=(8, 8), dpi=150, sharex=True)
    for profile in ["baseline", "geometric"]:
        error_values = [
            metric_value(profile_metrics, omega, profile, "mean_3d_error_m") for omega in omegas
        ]
        swing_values = [
            metric_value(profile_metrics, omega, profile, "mean_lateral_swing_m") for omega in omegas
        ]
        axes[0].plot(omegas, error_values, marker="o", label=profile)
        axes[1].plot(omegas, swing_values, marker="o", label=profile)

    axes[0].set_ylabel("mean 3D error [m]")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    axes[1].set_xlabel("Figure-8 angular rate omega [rad/s]")
    axes[1].set_ylabel("mean lateral swing [m]")
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()
    fig.suptitle("Controller Performance Across Figure-8 Speed")
    fig.tight_layout()
    fig.savefig(out_dir / "speed_sweep_tracking_swing.png")
    plt.close(fig)


def plot_improvements(out_dir, improvement_df, omegas):
    fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
    for metric in IMPROVEMENT_METRICS:
        values = [
            float(
                improvement_df[
                    (improvement_df["omega_rad_s"] == omega)
                    & (improvement_df["metric"] == metric)
                ].iloc[0]["improvement_percent"]
            )
            for omega in omegas
        ]
        ax.plot(omegas, values, marker="o", label=metric)

    ax.axhline(0.0, color="black", linewidth=1.0)
    ax.set_xlabel("Figure-8 angular rate omega [rad/s]")
    ax.set_ylabel("geometric improvement over baseline [%]")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.suptitle("Controller Improvement Across Speed Sweep")
    fig.tight_layout()
    fig.savefig(out_dir / "speed_sweep_improvement.png")
    plt.close(fig)


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


def write_report(out_dir, args, improvement_df, profile_metrics):
    selected_metrics = profile_metrics[profile_metrics["metric"].isin(IMPROVEMENT_METRICS)].copy()
    report = f"""# Controlled Figure-8 Speed Sweep - {date.today().isoformat()}

## Purpose

This experiment checks whether the tuned geometric controller advantage remains visible when the Figure-8 angular rate changes.

## Setup

- Vehicle: `iris_depth_payload`
- Payload: native ball-joint slung payload
- Controllers: PX4 position/velocity baseline and tuned geometric attitude/thrust controller
- Angular rates: `{", ".join(f"{omega:.2f}" for omega in args.omegas)} rad/s`
- Trials per speed and controller: `{args.trials}`
- Flight duration per trial: `{args.flight_duration_s:.1f} s`
- Geometric hover thrust: `{args.hover_thrust}`
- Validation gates: tracking sample count, PX4 local-position magnitude, steady altitude, and payload swing telemetry
- Raw per-trial telemetry CSV retention: `{args.keep_raw_telemetry}`

## Controller Improvement

{markdown_table(improvement_df, ["omega_rad_s", "metric", "baseline_mean", "geometric_mean", "improvement_percent"])}

## Profile Metrics

{markdown_table(selected_metrics, ["omega_rad_s", "profile", "metric", "mean", "std", "min", "max"])}

## Plots

- `speed_sweep_tracking_swing.png`
- `speed_sweep_improvement.png`

## Interpretation

This is a controlled screening sweep, not a final statistical campaign. It reuses the same validation gates as the repeatability phase and keeps all valid trials in the aggregate. Any speed with a weak or negative improvement should be treated as a controller-tuning target before expanding to larger batches.
"""
    (out_dir / "SPEED_SWEEP_SUMMARY.md").write_text(report)


def main():
    parser = argparse.ArgumentParser(description="Run controlled Figure-8 speed sweep validation.")
    parser.add_argument("--omegas", nargs="+", type=float, default=[0.15, 0.20, 0.25, 0.30])
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--flight-duration-s", type=float, default=75.0)
    parser.add_argument("--sitl-startup-s", type=float, default=22.0)
    parser.add_argument("--hover-thrust", type=float, default=0.72)
    parser.add_argument("--out-dir", default="reports/speed_sweep_validation_2026-07-22")
    parser.add_argument(
        "--keep-raw-telemetry",
        action="store_true",
        help="Keep large per-trial tracking and payload swing CSV files in the nested repeatability folders.",
    )
    args = parser.parse_args()

    repo_root = Path.cwd()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    metric_rows = []
    improvement_rows = []
    for omega in args.omegas:
        run_dir = out_dir / omega_label(omega)
        cmd = [
            "./tools/run_repeatability_validation.py",
            "--trials",
            str(args.trials),
            "--flight-duration-s",
            str(args.flight_duration_s),
            "--sitl-startup-s",
            str(args.sitl_startup_s),
            "--omega",
            str(omega),
            "--hover-thrust",
            str(args.hover_thrust),
            "--out-dir",
            str(run_dir),
        ]
        if args.keep_raw_telemetry:
            cmd.append("--keep-raw-telemetry")
        run_command(cmd, cwd=repo_root)

        metrics, improvements = collect_speed_rows(out_dir, omega)
        metric_rows.extend(metrics)
        improvement_rows.extend(improvements)

    profile_metrics = pd.DataFrame(metric_rows)
    improvement_df = pd.DataFrame(improvement_rows)
    profile_metrics.to_csv(out_dir / "speed_sweep_profile_metrics.csv", index=False)
    improvement_df.to_csv(out_dir / "speed_sweep_controller_improvement.csv", index=False)

    plot_tracking_and_swing(out_dir, profile_metrics, args.omegas)
    plot_improvements(out_dir, improvement_df, args.omegas)
    write_report(out_dir, args, improvement_df, profile_metrics)
    print(f"Speed sweep artifacts written to {out_dir}")


if __name__ == "__main__":
    main()
