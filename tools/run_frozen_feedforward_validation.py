#!/usr/bin/env python3
"""Randomized evaluation of the frozen wind feed-forward candidate."""

import argparse
import json
import random
import shutil
import subprocess
from datetime import date
from pathlib import Path

import pandas as pd

from experiment_provenance import relative_manifest_paths, write_manifest
from run_wind_envelope_validation import crosswind_world_name, write_crosswind_worlds
from statistical_analysis import bootstrap_improvement


METRICS = [
    "mean_3d_error_m",
    "rms_3d_error_m",
    "max_3d_error_m",
    "mean_lateral_swing_m",
    "mean_cable_angle_deg",
]


def wind_label(speed):
    return f"{speed:g}".replace(".", "p")


def build_runs(speeds, trials, seed):
    runs = [
        {"speed_m_s": speed, "profile": profile, "trial": trial}
        for speed in speeds
        for profile in ["baseline", "feedforward"]
        for trial in range(1, trials + 1)
    ]
    random.Random(seed).shuffle(runs)
    for sequence, run in enumerate(runs, start=1):
        run["sequence"] = sequence
        run["run_id"] = (
            f"wind_y{wind_label(run['speed_m_s'])}_{run['profile']}_trial_{run['trial']:02d}"
        )
    return runs


def run_command(command, cwd):
    print(" ".join(str(part) for part in command), flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def read_summary(run_dir):
    path = run_dir / "summary.json"
    return json.loads(path.read_text()) if path.exists() else None


def valid_summary(summary):
    return bool(summary and summary.get("tracking_valid") and summary.get("swing_valid"))


def summarize(trial_df):
    rows = []
    for (speed, profile), group in trial_df.groupby(["speed_m_s", "profile"]):
        for metric in METRICS:
            values = group[metric].astype(float)
            rows.append(
                {
                    "speed_m_s": speed,
                    "profile": profile,
                    "metric": metric,
                    "n": len(values),
                    "mean": values.mean(),
                    "std": values.std(ddof=1),
                    "min": values.min(),
                    "max": values.max(),
                }
            )
    return rows


def compare(trial_df, args):
    rows = []
    for speed_index, speed in enumerate(args.wind_speeds):
        speed_group = trial_df[trial_df["speed_m_s"] == speed]
        for metric_index, metric in enumerate(METRICS):
            baseline = speed_group[speed_group["profile"] == "baseline"][metric].astype(float)
            candidate = speed_group[speed_group["profile"] == "feedforward"][metric].astype(float)
            result = bootstrap_improvement(
                baseline,
                candidate,
                confidence_level=args.confidence_level,
                resamples=args.bootstrap_resamples,
                seed=args.bootstrap_seed + speed_index * 100 + metric_index,
            )
            rows.append({"speed_m_s": speed, "metric": metric, **result})
    return rows


def markdown_table(frame, columns):
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for _, row in frame[columns].iterrows():
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


def write_report(out_dir, args, aggregate_df, comparison_df):
    selected_aggregate = aggregate_df[aggregate_df["metric"].isin(METRICS)]
    report = f"""# Frozen Wind Feed-Forward Validation - {date.today().isoformat()}

## Protocol

- Candidate: disturbance observer gain `1.0`, cutoff `0.3 Hz`, limit `4.0 m/s^2`
- Payload swing gains: `kp=0.0`, `kd=0.0` (active swing feedback rejected during development)
- Geometric integral gains: `0.0`
- Winds: `{', '.join(f'{speed:g}' for speed in args.wind_speeds)} m/s`
- Trials: `{args.trials}` per controller per wind
- Total official flights: `{2 * args.trials * len(args.wind_speeds)}`
- Randomized-order seed: `{args.run_order_seed}`
- Bootstrap confidence: `{args.confidence_level:.0%}` with `{args.bootstrap_resamples}` resamples
- Raw telemetry retained: `true`

## Aggregate Metrics

{markdown_table(selected_aggregate, ["speed_m_s", "profile", "metric", "n", "mean", "std", "min", "max"])}

## Statistical Comparison

Positive improvement favors the frozen feed-forward candidate.

{markdown_table(comparison_df, ["speed_m_s", "metric", "absolute_improvement", "absolute_ci_low", "absolute_ci_high", "percent_improvement", "percent_ci_low", "percent_ci_high", "hedges_g"])}

## Interpretation Rule

The candidate is successful only where tracking improves without eliminating the payload-angle benefit. Negative or inconclusive results are retained and reported; this evaluation does not permit gain changes.
"""
    (out_dir / "FROZEN_FEEDFORWARD_VALIDATION_SUMMARY.md").write_text(report)


def main():
    parser = argparse.ArgumentParser(description="Run randomized validation of the frozen wind feed-forward candidate.")
    parser.add_argument("--wind-speeds", nargs="+", type=float, default=[0.0, 5.0, 10.0])
    parser.add_argument("--trials", type=int, default=5)
    parser.add_argument("--flight-duration-s", type=float, default=75.0)
    parser.add_argument("--sitl-startup-s", type=float, default=22.0)
    parser.add_argument("--run-order-seed", type=int, default=20_260_804)
    parser.add_argument("--bootstrap-seed", type=int, default=20_260_804)
    parser.add_argument("--bootstrap-resamples", type=int, default=10_000)
    parser.add_argument("--confidence-level", type=float, default=0.95)
    parser.add_argument("--repo-root", default="~/uav-autonomous-telemetry")
    parser.add_argument("--px4-dir", default="~/PX4-Autopilot")
    parser.add_argument("--out-dir", default="reports/wind_feedforward_swing_feedback_v1/frozen_validation")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.trials < 2:
        parser.error("--trials must be at least 2")

    runs = build_runs(args.wind_speeds, args.trials, args.run_order_seed)
    expected = 2 * len(args.wind_speeds) * args.trials
    if len(runs) != expected:
        raise RuntimeError(f"Expected {expected} runs, found {len(runs)}")
    if args.dry_run:
        print(json.dumps({"count": len(runs), "runs": runs}, indent=2))
        return

    repo_root = Path(args.repo_root).expanduser()
    px4_dir = Path(args.px4_dir).expanduser()
    out_dir = repo_root / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "run_order.json").write_text(json.dumps(runs, indent=2) + "\n")
    world_dir = px4_dir / "Tools/simulation/gazebo-classic/sitl_gazebo-classic/worlds"
    write_crosswind_worlds(world_dir, args.wind_speeds, [0.0, 1.0, 0.0])

    rows = []
    for run in runs:
        run_dir = out_dir / run["run_id"]
        summary = read_summary(run_dir) if args.resume else None
        if valid_summary(summary):
            print(f"Reusing valid run {run['sequence']}/{expected}: {run['run_id']}", flush=True)
        else:
            command = [
                "./tools/run_single_validation.py",
                "--profile", "geometric" if run["profile"] == "feedforward" else "baseline",
                "--flight-duration-s", str(args.flight_duration_s),
                "--sitl-startup-s", str(args.sitl_startup_s),
                "--omega", "0.25",
                "--world", crosswind_world_name(run["speed_m_s"]),
                "--out-dir", str(run_dir),
                "--min-samples", "500",
                "--target-altitude-ned", "-5.0",
                "--max-mean-altitude-error-m", "1.5",
            ]
            if run["profile"] == "feedforward":
                command.extend(
                    [
                        "--geometric-ki-xy", "0.0",
                        "--geometric-ki-z", "0.0",
                        "--geometric-integral-limit-xy", "5.0",
                        "--geometric-integral-limit-z", "2.0",
                        "--geometric-integrator-leak-rate", "0.02",
                        "--geometric-max-tilt-deg", "35.0",
                        "--geometric-kp-xy", "1.4",
                        "--geometric-kd-xy", "1.1",
                        "--disturbance-observer-gain", "1.0",
                        "--disturbance-filter-hz", "0.3",
                        "--disturbance-limit-xy", "4.0",
                        "--payload-swing-kp", "0.0",
                        "--payload-swing-kd", "0.0",
                        "--payload-correction-limit-xy", "0.75",
                    ]
                )
            print(f"Starting frozen validation {run['sequence']}/{expected}: {run['run_id']}", flush=True)
            run_command(command, repo_root)
            run_command(["./tools/plot_validation_run.py", str(run_dir)], repo_root)
            summary = read_summary(run_dir)
            if not valid_summary(summary):
                raise SystemExit(
                    f"{run['run_id']} failed telemetry validation: "
                    f"{summary.get('tracking_reason')} / {summary.get('swing_reason')}"
                )
            logs_dir = run_dir / "logs"
            if logs_dir.exists():
                shutil.rmtree(logs_dir)
        row = {**run, "tracking_valid": summary["tracking_valid"], "swing_valid": summary["swing_valid"]}
        for metric in METRICS:
            row[metric] = summary[metric]
        rows.append(row)

    trial_df = pd.DataFrame(rows).sort_values("sequence")
    aggregate_df = pd.DataFrame(summarize(trial_df))
    comparison_df = pd.DataFrame(compare(trial_df, args))
    trial_df.to_csv(out_dir / "feedforward_trial_metrics.csv", index=False)
    aggregate_df.to_csv(out_dir / "feedforward_aggregate_metrics.csv", index=False)
    comparison_df.to_csv(out_dir / "feedforward_statistical_comparison.csv", index=False)
    write_report(out_dir, args, aggregate_df, comparison_df)
    write_manifest(
        out_dir,
        experiment_type="frozen_wind_feedforward_validation",
        repo_root=repo_root,
        px4_dir=px4_dir,
        parameters={
            "profiles": ["baseline", "feedforward"],
            "wind_speeds_m_s": args.wind_speeds,
            "trials_per_profile_and_wind": args.trials,
            "run_order_seed": args.run_order_seed,
            "candidate_ki_xy": 0.0,
            "candidate_kd_xy": 1.1,
            "candidate_max_tilt_deg": 35.0,
            "candidate_disturbance_observer_gain": 1.0,
            "candidate_disturbance_filter_hz": 0.3,
            "candidate_disturbance_limit_xy": 4.0,
            "candidate_payload_swing_kp": 0.0,
            "candidate_payload_swing_kd": 0.0,
            "confidence_level": args.confidence_level,
            "bootstrap_resamples": args.bootstrap_resamples,
            "bootstrap_seed": args.bootstrap_seed,
        },
        data={
            "raw_telemetry_retention_policy": "retain",
            "constituent_manifests": relative_manifest_paths(out_dir),
            "run_order_json": "run_order.json",
            "trial_metrics_csv": "feedforward_trial_metrics.csv",
            "aggregate_metrics_csv": "feedforward_aggregate_metrics.csv",
            "statistical_comparison_csv": "feedforward_statistical_comparison.csv",
            "summary_markdown": "FROZEN_FEEDFORWARD_VALIDATION_SUMMARY.md",
        },
        result={
            "total_trials": int(len(trial_df)),
            "valid_tracking_trials": int(trial_df["tracking_valid"].sum()),
            "valid_swing_trials": int(trial_df["swing_valid"].sum()),
        },
    )
    print(f"Frozen wind feed-forward validation artifacts written to {out_dir}")


if __name__ == "__main__":
    main()
