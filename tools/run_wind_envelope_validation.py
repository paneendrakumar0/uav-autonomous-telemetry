#!/usr/bin/env python3
import argparse
import json
import math
import shutil
import subprocess
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


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


def run_command(cmd, cwd):
    print(" ".join(str(part) for part in cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, check=True)


def wind_label(speed):
    text = f"{speed:.1f}".rstrip("0").rstrip(".").replace(".", "p")
    return text or "0"


def crosswind_world_name(speed):
    return f"payload_crosswind_y{wind_label(speed)}"


def read_summary(run_dir):
    summary_path = run_dir / "summary.json"
    if not summary_path.exists():
        raise SystemExit(f"Missing summary file: {summary_path}")
    return json.loads(summary_path.read_text())


def reusable_summary(run_dir):
    summary_path = run_dir / "summary.json"
    if not summary_path.exists():
        return None
    summary = json.loads(summary_path.read_text())
    if "tracking_valid" in summary and "swing_valid" in summary:
        return summary
    return None


def remove_logs(run_dir):
    logs_dir = run_dir / "logs"
    if logs_dir.exists():
        shutil.rmtree(logs_dir)


def remove_raw_telemetry(run_dir):
    for csv_name in ["tracking_metrics.csv", "payload_swing_metrics.csv"]:
        path = run_dir / csv_name
        if path.exists():
            path.unlink()


def build_world_xml(speed, direction):
    direction_text = " ".join(str(value) for value in direction)
    sdf = ET.Element("sdf", {"version": "1.5"})
    world = ET.SubElement(sdf, "world", {"name": "default"})
    for model in ["sun", "ground_plane", "asphalt_plane"]:
        include = ET.SubElement(world, "include")
        ET.SubElement(include, "uri").text = f"model://{model}"

    plugin = ET.SubElement(world, "plugin", {"name": "wind_plugin", "filename": "libgazebo_wind_plugin.so"})
    fields = {
        "frameId": "base_link",
        "robotNamespace": "",
        "windVelocityMean": f"{speed:.6f}",
        "windVelocityMax": f"{speed:.6f}",
        "windVelocityVariance": "0",
        "windDirectionMean": direction_text,
        "windDirectionVariance": "0",
        "windGustStart": "0",
        "windGustDuration": "0",
        "windGustVelocityMean": "0",
        "windGustVelocityMax": "0",
        "windGustVelocityVariance": "0",
        "windGustDirectionMean": "1 0 0",
        "windGustDirectionVariance": "0",
        "windPubTopic": "world_wind",
    }
    for tag, value in fields.items():
        ET.SubElement(plugin, tag).text = value

    physics = ET.SubElement(world, "physics", {"name": "default_physics", "default": "0", "type": "ode"})
    ET.SubElement(physics, "gravity").text = "0 0 -9.8066"
    ode = ET.SubElement(physics, "ode")
    solver = ET.SubElement(ode, "solver")
    ET.SubElement(solver, "type").text = "quick"
    ET.SubElement(solver, "iters").text = "10"
    ET.SubElement(solver, "sor").text = "1.3"
    ET.SubElement(solver, "use_dynamic_moi_rescaling").text = "0"
    constraints = ET.SubElement(ode, "constraints")
    ET.SubElement(constraints, "cfm").text = "0"
    ET.SubElement(constraints, "erp").text = "0.2"
    ET.SubElement(constraints, "contact_max_correcting_vel").text = "100"
    ET.SubElement(constraints, "contact_surface_layer").text = "0.001"
    ET.SubElement(physics, "max_step_size").text = "0.004"
    ET.SubElement(physics, "real_time_factor").text = "1"
    ET.SubElement(physics, "real_time_update_rate").text = "250"
    ET.SubElement(physics, "magnetic_field").text = "6.0e-6 2.3e-5 -4.2e-5"

    ET.indent(sdf, space="  ")
    return ET.tostring(sdf, encoding="unicode") + "\n"


def write_crosswind_worlds(world_dir, speeds, direction):
    world_dir.mkdir(parents=True, exist_ok=True)
    for speed in speeds:
        world_path = world_dir / f"{crosswind_world_name(speed)}.world"
        world_path.write_text('<?xml version="1.0" ?>\n' + build_world_xml(speed, direction))


def summary_to_row(case, profile, summary):
    row = {
        "case": case["label"],
        "disturbance_type": case["type"],
        "wind_speed_m_s": case["speed_m_s"],
        "wind_direction": case["direction"],
        "profile": profile,
        "tracking_valid": bool(summary.get("tracking_valid", False)),
        "swing_valid": bool(summary.get("swing_valid", False)),
        "tracking_reason": summary.get("tracking_reason", ""),
        "world": summary.get("world", case["world"]),
    }
    for metric in METRICS:
        row[metric] = summary.get(metric)
    return row


def build_comparison_rows(profile_df):
    rows = []
    for case, group in profile_df.groupby("case"):
        if {"baseline", "geometric"} - set(group["profile"]):
            continue
        baseline = group[group["profile"] == "baseline"].iloc[0]
        geometric = group[group["profile"] == "geometric"].iloc[0]
        both_valid = bool(baseline["tracking_valid"]) and bool(geometric["tracking_valid"])
        for metric in COMPARISON_METRICS:
            b = baseline[metric]
            g = geometric[metric]
            improvement = None
            if both_valid and pd.notna(b) and pd.notna(g) and not math.isclose(float(b), 0.0):
                improvement = 100.0 * (float(b) - float(g)) / float(b)
            rows.append(
                {
                    "case": case,
                    "disturbance_type": baseline["disturbance_type"],
                    "wind_speed_m_s": float(baseline["wind_speed_m_s"]),
                    "metric": metric,
                    "baseline": b,
                    "geometric": g,
                    "both_tracking_valid": both_valid,
                    "improvement_percent": improvement,
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
            if pd.isna(value) or str(value).lower() == "nan":
                cells.append("n/a")
            elif isinstance(value, float):
                cells.append(f"{value:.4f}")
            else:
                cells.append(str(value))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def plot_metric_pair(out_dir, profile_df, metric, filename, ylabel):
    plot_df = profile_df[profile_df["disturbance_type"] == "crosswind_y"].copy()
    if plot_df.empty:
        return
    fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
    for profile in ["baseline", "geometric"]:
        sub = plot_df[plot_df["profile"] == profile].sort_values("wind_speed_m_s")
        if not sub.empty:
            ax.plot(sub["wind_speed_m_s"].to_numpy(), sub[metric].to_numpy(), marker="o", label=profile)
    ax.set_xlabel("constant Y-crosswind speed [m/s]")
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_dir / filename)
    plt.close(fig)


def plot_improvements(out_dir, comparison_df):
    plot_df = comparison_df[
        (comparison_df["disturbance_type"] == "crosswind_y")
        & (comparison_df["both_tracking_valid"])
        & (comparison_df["metric"].isin(COMPARISON_METRICS))
    ].copy()
    if plot_df.empty:
        return
    fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
    for metric in COMPARISON_METRICS:
        sub = plot_df[plot_df["metric"] == metric].sort_values("wind_speed_m_s")
        if not sub.empty:
            ax.plot(
                sub["wind_speed_m_s"].to_numpy(),
                sub["improvement_percent"].to_numpy(),
                marker="o",
                label=metric,
            )
    ax.axhline(0.0, color="black", linewidth=1.0)
    ax.set_xlabel("constant Y-crosswind speed [m/s]")
    ax.set_ylabel("geometric improvement over baseline [%]")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out_dir / "wind_envelope_improvement.png")
    plt.close(fig)


def write_report(out_dir, args, cases, profile_df, comparison_df):
    selected_profile = profile_df[
        [
            "case",
            "profile",
            "tracking_valid",
            "mean_3d_error_m",
            "rms_3d_error_m",
            "mean_lateral_swing_m",
            "mean_cable_angle_deg",
            "tracking_reason",
        ]
    ]
    report = f"""# Wind Disturbance Envelope Screening - {date.today().isoformat()}

## Purpose

This phase turns the first wind tests into a repeatable disturbance-envelope workflow. The objective is to evaluate how the PX4 position/velocity baseline and the tuned geometric attitude/thrust controller degrade under external aerodynamic disturbance.

## Setup

- Vehicle: `iris_depth_payload`
- Payload: nominal `0.05 kg`, `1.0 m` cable
- Trajectory: Figure-8
- Angular rate: `{args.omega} rad/s`
- Controllers: PX4 position/velocity baseline and tuned geometric attitude/thrust controller
- Constant crosswind direction: `{args.direction}`
- Crosswind speeds prepared for the envelope: `{", ".join(f"{speed:.1f}" for speed in args.crosswind_speeds)} m/s`
- Existing screening imports enabled: `{args.import_existing_screening}`
- Raw per-trial telemetry retention: `{args.keep_raw_telemetry}`

## Disturbance Cases

{markdown_table(pd.DataFrame(cases), ["label", "type", "speed_m_s", "world", "source"])}

## Profile Metrics

{markdown_table(selected_profile, selected_profile.columns.tolist())}

## Controller Comparison

{markdown_table(comparison_df, ["case", "metric", "baseline", "geometric", "both_tracking_valid", "improvement_percent"])}

## Plots

- `wind_envelope_tracking_error.png`
- `wind_envelope_payload_swing.png`
- `wind_envelope_improvement.png`

## Interpretation

The current wind evidence shows that the controller tradeoff is disturbance-dependent. Under constant Y-crosswind, the geometric controller reduces payload swing but loses substantial path-tracking accuracy relative to PX4. Under a finite Y-gust, it improves average tracking and swing but produces larger peak excursions. Under vertical updraft, PX4 baseline fails the altitude validation gate while the geometric controller completes the circuit with altitude bias.

This is now ready to expand into a true envelope campaign by filling the generated constant-crosswind worlds at multiple wind speeds. The important research question for the next batch is not whether the vehicle flies once, but where each controller crosses from acceptable tracking into degraded or failed behavior.
"""
    (out_dir / "WIND_DISTURBANCE_ENVELOPE_SUMMARY.md").write_text(report)


def imported_screening_cases(repo_root):
    return [
        {
            "label": "crosswind_y5",
            "type": "crosswind_y",
            "speed_m_s": 5.0,
            "direction": "0 1 0",
            "world": "payload_crosswind_y5",
            "source": "reports/wind_disturbance_crosswind_y5_2026-07-25",
            "baseline_dir": repo_root / "reports/wind_disturbance_crosswind_y5_2026-07-25/baseline_crosswind_y5",
            "geometric_dir": repo_root / "reports/wind_disturbance_crosswind_y5_2026-07-25/geometric_crosswind_y5",
        },
        {
            "label": "gust_y10",
            "type": "gust_y",
            "speed_m_s": 10.0,
            "direction": "0 1 0",
            "world": "payload_gust_y10",
            "source": "reports/wind_disturbance_gust_y10_2026-07-25",
            "baseline_dir": repo_root / "reports/wind_disturbance_gust_y10_2026-07-25/baseline_gust_y10",
            "geometric_dir": repo_root / "reports/wind_disturbance_gust_y10_2026-07-25/geometric_gust_y10",
        },
        {
            "label": "updraft_z5",
            "type": "updraft_z",
            "speed_m_s": 5.0,
            "direction": "0 0 1",
            "world": "payload_updraft_z5",
            "source": "reports/wind_disturbance_updraft_z5_2026-07-25",
            "baseline_dir": repo_root / "reports/wind_disturbance_updraft_z5_2026-07-25/baseline_updraft_z5",
            "geometric_dir": repo_root / "reports/wind_disturbance_updraft_z5_2026-07-25/geometric_updraft_z5",
        },
    ]


def main():
    parser = argparse.ArgumentParser(description="Run or summarize wind-envelope validation for the slung-payload Figure-8.")
    parser.add_argument("--crosswind-speeds", nargs="+", type=float, default=[0.0, 2.5, 5.0, 7.5, 10.0])
    parser.add_argument("--direction", nargs=3, type=float, default=[0.0, 1.0, 0.0])
    parser.add_argument("--omega", type=float, default=0.25)
    parser.add_argument("--hover-thrust", type=float, default=0.72)
    parser.add_argument("--flight-duration-s", type=float, default=75.0)
    parser.add_argument("--sitl-startup-s", type=float, default=22.0)
    parser.add_argument("--repo-root", default="~/uav-autonomous-telemetry")
    parser.add_argument("--px4-dir", default="~/PX4-Autopilot")
    parser.add_argument("--out-dir", default=f"reports/wind_envelope_validation_{date.today().isoformat()}")
    parser.add_argument("--run-sim", action="store_true", help="Run the generated constant-crosswind cases.")
    parser.add_argument("--resume", action="store_true", help="Reuse already existing summaries in the output folder.")
    parser.add_argument("--import-existing-screening", action="store_true", help="Import the existing 2026-07-25 wind screening trials.")
    parser.add_argument("--keep-raw-telemetry", action="store_true")
    parser.add_argument("--gui", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).expanduser()
    px4_dir = Path(args.px4_dir).expanduser()
    out_dir = repo_root / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    world_dir = px4_dir / "Tools/simulation/gazebo-classic/sitl_gazebo-classic/worlds"
    write_crosswind_worlds(world_dir, args.crosswind_speeds, args.direction)

    cases = []
    rows = []
    if args.import_existing_screening:
        for case in imported_screening_cases(repo_root):
            cases.append({key: case[key] for key in ["label", "type", "speed_m_s", "direction", "world", "source"]})
            rows.append(summary_to_row(case, "baseline", read_summary(case["baseline_dir"])))
            rows.append(summary_to_row(case, "geometric", read_summary(case["geometric_dir"])))

    if args.run_sim:
        for speed in args.crosswind_speeds:
            label = f"crosswind_y{wind_label(speed)}"
            world = crosswind_world_name(speed)
            case = {
                "label": label,
                "type": "crosswind_y",
                "speed_m_s": speed,
                "direction": " ".join(str(value) for value in args.direction),
                "world": world,
                "source": "generated_run",
            }
            cases.append(case)
            for profile in ["baseline", "geometric"]:
                run_dir = out_dir / f"{label}_{profile}"
                summary = reusable_summary(run_dir) if args.resume else None
                if summary is None:
                    cmd = [
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
                        "--world",
                        world,
                        "--out-dir",
                        str(run_dir),
                        "--min-samples",
                        "500",
                        "--target-altitude-ned",
                        "-5.0",
                        "--max-mean-altitude-error-m",
                        "1.5",
                    ]
                    if args.gui:
                        cmd.append("--gui")
                    run_command(cmd, cwd=repo_root)
                    run_command(["./tools/plot_validation_run.py", str(run_dir)], cwd=repo_root)
                    remove_logs(run_dir)
                    if not args.keep_raw_telemetry:
                        remove_raw_telemetry(run_dir)
                    summary = read_summary(run_dir)
                rows.append(summary_to_row(case, profile, summary))

    if not rows:
        raise SystemExit("No wind data available. Use --run-sim and/or --import-existing-screening.")

    profile_df = pd.DataFrame(rows)
    comparison_df = pd.DataFrame(build_comparison_rows(profile_df))
    profile_df.to_csv(out_dir / "wind_envelope_profile_metrics.csv", index=False)
    comparison_df.to_csv(out_dir / "wind_envelope_controller_comparison.csv", index=False)
    (out_dir / "wind_envelope_cases.json").write_text(json.dumps(cases, indent=2) + "\n")

    plot_metric_pair(out_dir, profile_df, "mean_3d_error_m", "wind_envelope_tracking_error.png", "mean 3D tracking error [m]")
    plot_metric_pair(out_dir, profile_df, "mean_lateral_swing_m", "wind_envelope_payload_swing.png", "mean lateral swing [m]")
    plot_improvements(out_dir, comparison_df)
    write_report(out_dir, args, cases, profile_df, comparison_df)
    print(f"Wind-envelope artifacts written to {out_dir}")


if __name__ == "__main__":
    main()
