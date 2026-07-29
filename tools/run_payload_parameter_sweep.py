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

from experiment_provenance import (
    mark_raw_telemetry_discarded,
    relative_manifest_paths,
    write_manifest,
)


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

COMPARISON_METRICS = [
    "mean_3d_error_m",
    "rms_3d_error_m",
    "mean_lateral_swing_m",
    "mean_cable_angle_deg",
]


def run_command(cmd, cwd):
    print(" ".join(str(part) for part in cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, check=True)


def case_label(mass_kg, cable_length_m):
    return f"m{int(round(mass_kg * 1000)):03d}_l{int(round(cable_length_m * 100)):03d}"


def remove_logs(run_dir):
    logs_dir = run_dir / "logs"
    if logs_dir.exists():
        shutil.rmtree(logs_dir)


def remove_raw_telemetry(run_dir):
    removed = []
    for csv_name in ["tracking_metrics.csv", "payload_swing_metrics.csv"]:
        path = run_dir / csv_name
        if path.exists():
            path.unlink()
            removed.append(csv_name)
    mark_raw_telemetry_discarded(run_dir, removed)


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
    if summary.get("tracking_valid", False) and summary.get("swing_valid", False):
        return summary
    return None


def find_named_element(parent, tag, name):
    for element in parent.findall(tag):
        if element.attrib.get("name") == name:
            return element
    raise SystemExit(f"Could not find <{tag} name='{name}'> in SDF")


def set_text(element, value):
    element.text = str(value)


def set_payload_sdf(sdf_path, mass_kg, cable_length_m, payload_radius_m):
    tree = ET.parse(sdf_path)
    root = tree.getroot()
    model = root.find("model")
    if model is None:
        raise SystemExit(f"Missing model element in {sdf_path}")

    payload = find_named_element(model, "link", "slung_payload")
    joint = find_named_element(model, "joint", "slung_payload_joint")
    cable_visual = find_named_element(payload, "visual", "payload_cable_visual")
    payload_visual = find_named_element(payload, "visual", "slung_payload_visual")

    set_text(payload.find("pose"), f"0 0 -{cable_length_m:.6f} 0 0 0")
    set_text(payload.find("inertial/mass"), f"{mass_kg:.6f}")

    inertia = 0.4 * mass_kg * payload_radius_m * payload_radius_m
    for key in ["ixx", "iyy", "izz"]:
        set_text(payload.find(f"inertial/inertia/{key}"), f"{inertia:.8f}")
    for key in ["ixy", "ixz", "iyz"]:
        set_text(payload.find(f"inertial/inertia/{key}"), "0")

    set_text(payload_visual.find("geometry/sphere/radius"), f"{payload_radius_m:.6f}")
    set_text(cable_visual.find("pose"), f"0 0 {0.5 * cable_length_m:.6f} 0 0 0")
    set_text(cable_visual.find("geometry/cylinder/length"), f"{cable_length_m:.6f}")
    set_text(joint.find("pose"), f"0 0 {cable_length_m:.6f} 0 0 0")

    ET.indent(tree, space="  ")
    tree.write(sdf_path, encoding="utf-8", xml_declaration=False)


def validate_summary(label, summary):
    if not summary.get("tracking_valid", False) or not summary.get("swing_valid", False):
        raise SystemExit(
            f"{label} failed validation: "
            f"{summary.get('tracking_reason')} / {summary.get('swing_reason')}"
        )


def profile_rows(case, profile, summary):
    row = {
        "case": case["label"],
        "payload_mass_kg": case["mass_kg"],
        "cable_length_m": case["cable_length_m"],
        "profile": profile,
        "tracking_valid": summary["tracking_valid"],
        "swing_valid": summary["swing_valid"],
    }
    for metric in TRACKING_METRICS + SWING_METRICS:
        row[metric] = summary.get(metric)
    return row


def comparison_rows(profile_df):
    rows = []
    for case, group in profile_df.groupby("case"):
        baseline = group[group["profile"] == "baseline"].iloc[0]
        geometric = group[group["profile"] == "geometric"].iloc[0]
        for metric in COMPARISON_METRICS:
            b = float(baseline[metric])
            g = float(geometric[metric])
            rows.append(
                {
                    "case": case,
                    "payload_mass_kg": float(baseline["payload_mass_kg"]),
                    "cable_length_m": float(baseline["cable_length_m"]),
                    "metric": metric,
                    "baseline": b,
                    "geometric": g,
                    "improvement_percent": 100.0 * (b - g) / b if not math.isclose(b, 0.0) else 0.0,
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


def plot_case_metric(out_dir, comparison_df, metric, filename, ylabel):
    metric_df = comparison_df[comparison_df["metric"] == metric].copy()
    fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
    labels = metric_df["case"].tolist()
    x = range(len(labels))
    width = 0.36
    ax.bar([i - width / 2 for i in x], metric_df["baseline"], width=width, label="baseline")
    ax.bar([i + width / 2 for i in x], metric_df["geometric"], width=width, label="geometric")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, rotation=25, ha="right")
    ax.set_ylabel(ylabel)
    ax.grid(True, axis="y", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_dir / filename)
    plt.close(fig)


def plot_improvement(out_dir, comparison_df):
    fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
    for metric in COMPARISON_METRICS:
        metric_df = comparison_df[comparison_df["metric"] == metric]
        ax.plot(
            metric_df["case"].to_list(),
            metric_df["improvement_percent"].to_numpy(),
            marker="o",
            label=metric,
        )
    ax.axhline(0.0, color="black", linewidth=1.0)
    ax.set_ylabel("geometric improvement over baseline [%]")
    ax.set_xlabel("payload case")
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis="x", rotation=25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out_dir / "payload_parameter_improvement.png")
    plt.close(fig)


def write_report(out_dir, args, cases, profile_df, comparison_df):
    report = f"""# Payload Parameter Screening Sweep - {date.today().isoformat()}

## Purpose

This screening phase checks whether the controller comparison remains valid when the physical slung payload parameters change. It intentionally varies one physical parameter at a time around the previously validated nominal case.

## Setup

- Vehicle: `iris_depth_payload`
- Trajectory: Figure-8
- Angular rate: `{args.omega} rad/s`
- Controllers: PX4 position/velocity baseline and tuned geometric attitude/thrust controller
- Payload model: native ball-joint `base_link -> slung_payload`
- Payload radius: `{args.payload_radius_m} m`
- Trials per case and controller: `1`
- Raw telemetry retention: `{args.keep_raw_telemetry}`
- Live PX4 SDF restored after the sweep: `true`

## Cases

{markdown_table(pd.DataFrame(cases), ["label", "mass_kg", "cable_length_m", "reason"])}

## Profile Metrics

{markdown_table(profile_df, ["case", "profile", "tracking_valid", "swing_valid", "mean_3d_error_m", "rms_3d_error_m", "mean_lateral_swing_m", "mean_cable_angle_deg"])}

## Controller Comparison

{markdown_table(comparison_df, ["case", "metric", "baseline", "geometric", "improvement_percent"])}

## Plots

- `payload_parameter_tracking_error.png`
- `payload_parameter_swing.png`
- `payload_parameter_improvement.png`

## Interpretation

This is a screening dataset, not the final payload robustness campaign. It is meant to identify which payload changes are safe for larger repeatability batches and which cases expose controller limits. All valid cases are retained in the comparison.
"""
    (out_dir / "PAYLOAD_PARAMETER_SWEEP_SUMMARY.md").write_text(report)


def default_cases():
    return [
        {"label": "nominal_m050_l100", "mass_kg": 0.05, "cable_length_m": 1.0, "reason": "validated nominal payload"},
        {"label": "mass_m100_l100", "mass_kg": 0.10, "cable_length_m": 1.0, "reason": "double payload mass"},
        {"label": "mass_m200_l100", "mass_kg": 0.20, "cable_length_m": 1.0, "reason": "quadruple payload mass"},
        {"label": "cable_m050_l050", "mass_kg": 0.05, "cable_length_m": 0.5, "reason": "short cable"},
        {"label": "cable_m050_l150", "mass_kg": 0.05, "cable_length_m": 1.5, "reason": "long cable"},
    ]


def main():
    parser = argparse.ArgumentParser(description="Run controlled slung-payload mass/cable screening sweep.")
    parser.add_argument("--omega", type=float, default=0.25)
    parser.add_argument("--hover-thrust", type=float, default=0.72)
    parser.add_argument("--flight-duration-s", type=float, default=75.0)
    parser.add_argument("--sitl-startup-s", type=float, default=22.0)
    parser.add_argument("--payload-radius-m", type=float, default=0.10)
    parser.add_argument("--repo-root", default="~/uav-autonomous-telemetry")
    parser.add_argument("--px4-dir", default="~/PX4-Autopilot")
    parser.add_argument("--out-dir", default="reports/payload_parameter_sweep_2026-07-22")
    retention = parser.add_mutually_exclusive_group()
    retention.add_argument(
        "--keep-raw-telemetry",
        dest="keep_raw_telemetry",
        action="store_true",
        default=True,
        help="Keep per-run tracking and payload swing CSV files (default).",
    )
    retention.add_argument(
        "--discard-raw-telemetry",
        dest="keep_raw_telemetry",
        action="store_false",
        help="Delete per-run raw telemetry CSV files after aggregation.",
    )
    parser.add_argument("--resume", action="store_true", help="Reuse already valid case/profile summaries in the output folder.")
    parser.add_argument("--gui", action="store_true", help="Open Gazebo Classic while each validation trial runs.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).expanduser()
    px4_dir = Path(args.px4_dir).expanduser()
    out_dir = repo_root / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    sdf_path = (
        px4_dir
        / "Tools/simulation/gazebo-classic/sitl_gazebo-classic/models/iris_depth_payload/iris_depth_payload.sdf"
    )
    original_sdf = sdf_path.read_text()
    (out_dir / "original_iris_depth_payload.sdf").write_text(original_sdf)

    cases = default_cases()
    (out_dir / "payload_cases.json").write_text(json.dumps(cases, indent=2) + "\n")

    rows = []
    try:
        for case in cases:
            set_payload_sdf(
                sdf_path,
                mass_kg=case["mass_kg"],
                cable_length_m=case["cable_length_m"],
                payload_radius_m=args.payload_radius_m,
            )
            for profile in ["baseline", "geometric"]:
                label = f"{case['label']}_{profile}"
                run_dir = out_dir / label
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
                            "--out-dir",
                            str(run_dir),
                            "--min-samples",
                            "500",
                            "--target-altitude-ned",
                            "-5.0",
                            "--max-mean-altitude-error-m",
                            "1.0",
                        ]
                    if args.gui:
                        cmd.append("--gui")
                    run_command(cmd, cwd=repo_root)
                    run_command(["./tools/plot_validation_run.py", str(run_dir)], cwd=repo_root)
                    remove_logs(run_dir)

                    summary = read_summary(run_dir)
                    validate_summary(label, summary)
                    if not args.keep_raw_telemetry:
                        remove_raw_telemetry(run_dir)
                else:
                    print(f"Reusing valid run: {run_dir}", flush=True)
                rows.append(profile_rows(case, profile, summary))
    finally:
        sdf_path.write_text(original_sdf)

    profile_df = pd.DataFrame(rows)
    profile_df.to_csv(out_dir / "payload_parameter_profile_metrics.csv", index=False)
    comparison_df = pd.DataFrame(comparison_rows(profile_df))
    comparison_df.to_csv(out_dir / "payload_parameter_controller_comparison.csv", index=False)

    plot_case_metric(
        out_dir,
        comparison_df,
        "mean_3d_error_m",
        "payload_parameter_tracking_error.png",
        "mean 3D tracking error [m]",
    )
    plot_case_metric(
        out_dir,
        comparison_df,
        "mean_lateral_swing_m",
        "payload_parameter_swing.png",
        "mean lateral swing [m]",
    )
    plot_improvement(out_dir, comparison_df)
    write_report(out_dir, args, cases, profile_df, comparison_df)
    write_manifest(
        out_dir,
        experiment_type="payload_parameter_sweep",
        repo_root=repo_root,
        px4_dir=px4_dir,
        parameters={
            "profiles": ["baseline", "geometric"],
            "omega_rad_s": args.omega,
            "hover_thrust": args.hover_thrust,
            "flight_duration_s": args.flight_duration_s,
            "sitl_startup_s": args.sitl_startup_s,
            "payload_radius_m": args.payload_radius_m,
            "cases": cases,
            "resume_enabled": args.resume,
        },
        data={
            "raw_telemetry_retention_policy": (
                "retain" if args.keep_raw_telemetry else "discard_after_aggregation"
            ),
            "constituent_manifests": relative_manifest_paths(out_dir),
            "case_definitions_json": "payload_cases.json",
            "original_payload_sdf": "original_iris_depth_payload.sdf",
            "profile_metrics_csv": "payload_parameter_profile_metrics.csv",
            "controller_comparison_csv": "payload_parameter_controller_comparison.csv",
            "summary_markdown": "PAYLOAD_PARAMETER_SWEEP_SUMMARY.md",
        },
        result={
            "case_count": len(cases),
            "profile_runs": int(len(profile_df)),
            "valid_tracking_runs": int(profile_df["tracking_valid"].sum()),
            "valid_swing_runs": int(profile_df["swing_valid"].sum()),
        },
    )
    print(f"Payload parameter sweep artifacts written to {out_dir}")


if __name__ == "__main__":
    main()
