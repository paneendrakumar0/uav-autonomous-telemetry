#!/usr/bin/env python3
"""Run the exact 32-flight screening matrix that follows nominal repeatability."""

import argparse
import json
import math
import random
import shutil
import subprocess
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

import pandas as pd

from experiment_provenance import relative_manifest_paths, write_manifest
from run_payload_parameter_sweep import set_payload_sdf
from run_wind_envelope_validation import build_world_xml, crosswind_world_name, write_crosswind_worlds


METRICS = [
    "mean_3d_error_m",
    "rms_3d_error_m",
    "max_3d_error_m",
    "mean_lateral_swing_m",
    "max_lateral_swing_m",
    "mean_cable_angle_deg",
    "max_cable_angle_deg",
]
COMPARISON_METRICS = [
    "mean_3d_error_m",
    "rms_3d_error_m",
    "mean_lateral_swing_m",
    "mean_cable_angle_deg",
]


def build_run_matrix():
    runs = []

    def add_pair(family, case, **parameters):
        for profile in ["baseline", "geometric"]:
            runs.append(
                {
                    "run_id": f"{family}_{case}_{profile}",
                    "family": family,
                    "case": case,
                    "profile": profile,
                    "omega_rad_s": 0.25,
                    "altitude_ned_m": -5.0,
                    "payload_mass_kg": 0.05,
                    "cable_length_m": 1.0,
                    "world": "",
                    **parameters,
                }
            )

    for speed in [0.0, 2.5, 5.0, 7.5, 10.0]:
        label = str(speed).rstrip("0").rstrip(".").replace(".", "p") or "0"
        add_pair(
            "wind",
            f"crosswind_y{label}",
            wind_speed_m_s=speed,
            world=crosswind_world_name(speed),
        )
    for altitude_m in [3.0, 5.0, 7.0]:
        add_pair("altitude", f"altitude_{int(altitude_m)}m", altitude_ned_m=-altitude_m)
    for omega in [0.20, 0.25, 0.30]:
        add_pair("speed", f"omega_{int(round(omega * 100)):03d}", omega_rad_s=omega)
    for mass in [0.05, 0.10, 0.20]:
        add_pair("payload", f"mass_{int(round(mass * 1000)):03d}g", payload_mass_kg=mass)
    add_pair("stress", "gust_y10", wind_speed_m_s=10.0, world="payload_gust_y10")
    add_pair("stress", "updraft_z5", wind_speed_m_s=5.0, world="payload_updraft_z5")

    if len(runs) != 32:
        raise RuntimeError(f"Campaign matrix must contain exactly 32 runs, found {len(runs)}")
    return runs


def write_stress_world(world_dir, name, mean_speed, mean_direction, gust_speed=0.0, gust_direction=None):
    root = ET.fromstring(build_world_xml(mean_speed, mean_direction))
    plugin = root.find(".//plugin[@name='wind_plugin']")
    if plugin is None:
        raise RuntimeError("Generated wind world is missing wind_plugin")
    if gust_speed > 0.0:
        values = {
            "windGustStart": "10",
            "windGustDuration": "20",
            "windGustVelocityMean": f"{gust_speed:.6f}",
            "windGustVelocityMax": f"{gust_speed:.6f}",
            "windGustVelocityVariance": "0",
            "windGustDirectionMean": " ".join(str(value) for value in gust_direction),
            "windGustDirectionVariance": "0",
        }
        for tag, value in values.items():
            plugin.find(tag).text = value
    ET.indent(root, space="  ")
    (world_dir / f"{name}.world").write_text(
        '<?xml version="1.0" ?>\n' + ET.tostring(root, encoding="unicode") + "\n"
    )


def prepare_worlds(px4_dir):
    world_dir = px4_dir / "Tools/simulation/gazebo-classic/sitl_gazebo-classic/worlds"
    write_crosswind_worlds(world_dir, [0.0, 2.5, 5.0, 7.5, 10.0], [0.0, 1.0, 0.0])
    write_stress_world(
        world_dir,
        "payload_gust_y10",
        0.0,
        [0.0, 1.0, 0.0],
        gust_speed=10.0,
        gust_direction=[0.0, 1.0, 0.0],
    )
    write_stress_world(world_dir, "payload_updraft_z5", 5.0, [0.0, 0.0, 1.0])


def read_summary(run_dir):
    path = run_dir / "summary.json"
    if not path.exists():
        return None
    return json.loads(path.read_text())


def valid_summary(summary):
    return bool(summary and summary.get("tracking_valid") and summary.get("swing_valid"))


def run_command(command, cwd):
    print(" ".join(str(part) for part in command), flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def row_from_summary(run, summary):
    row = {**run, "tracking_valid": summary["tracking_valid"], "swing_valid": summary["swing_valid"]}
    for metric in METRICS:
        row[metric] = summary.get(metric)
    return row


def comparison_rows(metrics_df):
    rows = []
    for (family, case), group in metrics_df.groupby(["family", "case"], sort=False):
        baseline = group[group["profile"] == "baseline"].iloc[0]
        geometric = group[group["profile"] == "geometric"].iloc[0]
        for metric in COMPARISON_METRICS:
            base_value = float(baseline[metric])
            candidate_value = float(geometric[metric])
            improvement = math.nan
            if not math.isclose(base_value, 0.0):
                improvement = 100.0 * (base_value - candidate_value) / base_value
            rows.append(
                {
                    "family": family,
                    "case": case,
                    "metric": metric,
                    "baseline": base_value,
                    "geometric": candidate_value,
                    "improvement_percent": improvement,
                }
            )
    return rows


def markdown_table(frame, columns):
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for _, row in frame[columns].iterrows():
        values = []
        for value in row:
            values.append(f"{value:.4f}" if isinstance(value, float) else str(value))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_report(out_dir, args, metrics_df, comparison_df):
    selected = comparison_df[comparison_df["metric"].isin(["mean_3d_error_m", "mean_cable_angle_deg"])]
    report = f"""# Remaining 32-Run Validation Matrix - {date.today().isoformat()}

## Protocol

- Deterministic randomized run-order seed: `{args.run_order_seed}`
- Flight duration: `{args.flight_duration_s:.1f} s`
- Profiles: PX4 baseline and geometric attitude/thrust
- Families: 10 wind, 6 altitude, 6 speed, 6 payload-mass, 4 gust/updraft runs
- Raw telemetry retained: `true`
- Completed valid runs: `{len(metrics_df)}/32`

## Per-run Metrics

{markdown_table(metrics_df, ["sequence", "family", "case", "profile", "tracking_valid", "swing_valid", "mean_3d_error_m", "mean_cable_angle_deg"])}

## Paired Controller Comparison

Positive improvement favors the geometric controller.

{markdown_table(selected, ["family", "case", "metric", "baseline", "geometric", "improvement_percent"])}
"""
    (out_dir / "REMAINING_CAMPAIGN_SUMMARY.md").write_text(report)


def main():
    parser = argparse.ArgumentParser(description="Run the exact remaining 32 flights of the 42-run campaign.")
    parser.add_argument("--repo-root", default="~/uav-autonomous-telemetry")
    parser.add_argument("--px4-dir", default="~/PX4-Autopilot")
    parser.add_argument("--out-dir", default="reports/validation_campaign_42_2026-08-02/02_remaining_matrix")
    parser.add_argument("--flight-duration-s", type=float, default=75.0)
    parser.add_argument("--sitl-startup-s", type=float, default=22.0)
    parser.add_argument("--run-order-seed", type=int, default=20_260_802)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    runs = build_run_matrix()
    random.Random(args.run_order_seed).shuffle(runs)
    for sequence, run in enumerate(runs, start=11):
        run["sequence"] = sequence

    if args.dry_run:
        print(json.dumps({"count": len(runs), "runs": runs}, indent=2))
        return

    repo_root = Path(args.repo_root).expanduser()
    px4_dir = Path(args.px4_dir).expanduser()
    out_dir = repo_root / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "run_order.json").write_text(json.dumps(runs, indent=2) + "\n")
    prepare_worlds(px4_dir)

    sdf_path = px4_dir / "Tools/simulation/gazebo-classic/sitl_gazebo-classic/models/iris_depth_payload/iris_depth_payload.sdf"
    original_sdf = sdf_path.read_text()
    (out_dir / "original_iris_depth_payload.sdf").write_text(original_sdf)
    rows = []
    try:
        for run in runs:
            run_dir = out_dir / run["run_id"]
            summary = read_summary(run_dir) if args.resume else None
            if valid_summary(summary):
                print(f"Reusing valid run {run['sequence']}/42: {run['run_id']}", flush=True)
            else:
                set_payload_sdf(
                    sdf_path,
                    mass_kg=run["payload_mass_kg"],
                    cable_length_m=run["cable_length_m"],
                    payload_radius_m=0.10,
                )
                command = [
                    "./tools/run_single_validation.py",
                    "--profile", run["profile"],
                    "--flight-duration-s", str(args.flight_duration_s),
                    "--sitl-startup-s", str(args.sitl_startup_s),
                    "--omega", str(run["omega_rad_s"]),
                    "--target-altitude-ned", str(run["altitude_ned_m"]),
                    "--out-dir", str(run_dir),
                    "--min-samples", "500",
                    "--max-mean-altitude-error-m", "1.5" if run["family"] in {"wind", "stress"} else "1.0",
                ]
                if run["world"]:
                    command.extend(["--world", run["world"]])
                print(f"Starting randomized run {run['sequence']}/42: {run['run_id']}", flush=True)
                run_command(command, repo_root)
                run_command(["./tools/plot_validation_run.py", str(run_dir)], repo_root)
                summary = read_summary(run_dir)
                if not valid_summary(summary):
                    raise SystemExit(
                        f"{run['run_id']} failed validation: "
                        f"{summary.get('tracking_reason')} / {summary.get('swing_reason')}"
                    )
                logs_dir = run_dir / "logs"
                if logs_dir.exists():
                    shutil.rmtree(logs_dir)
            rows.append(row_from_summary(run, summary))
    finally:
        sdf_path.write_text(original_sdf)

    metrics_df = pd.DataFrame(rows).sort_values("sequence")
    comparison_df = pd.DataFrame(comparison_rows(metrics_df))
    metrics_df.to_csv(out_dir / "remaining_run_metrics.csv", index=False)
    comparison_df.to_csv(out_dir / "remaining_controller_comparison.csv", index=False)
    write_report(out_dir, args, metrics_df, comparison_df)
    write_manifest(
        out_dir,
        experiment_type="remaining_32_run_campaign_matrix",
        repo_root=repo_root,
        px4_dir=px4_dir,
        parameters={
            "run_order_seed": args.run_order_seed,
            "flight_duration_s": args.flight_duration_s,
            "sitl_startup_s": args.sitl_startup_s,
            "run_count": len(runs),
            "families": {"wind": 10, "altitude": 6, "speed": 6, "payload": 6, "stress": 4},
        },
        data={
            "raw_telemetry_retention_policy": "retain",
            "constituent_manifests": relative_manifest_paths(out_dir),
            "run_order_json": "run_order.json",
            "run_metrics_csv": "remaining_run_metrics.csv",
            "controller_comparison_csv": "remaining_controller_comparison.csv",
            "summary_markdown": "REMAINING_CAMPAIGN_SUMMARY.md",
        },
        result={
            "total_runs": int(len(metrics_df)),
            "valid_tracking_runs": int(metrics_df["tracking_valid"].sum()),
            "valid_swing_runs": int(metrics_df["swing_valid"].sum()),
        },
    )
    print(f"Remaining campaign artifacts written to {out_dir}")


if __name__ == "__main__":
    main()
