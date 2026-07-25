#!/usr/bin/env python3
import argparse
import json
import os
import signal
import subprocess
import time
from datetime import datetime
from pathlib import Path

import pandas as pd


def terminate_process(proc, sig=signal.SIGINT):
    if proc is None or proc.poll() is not None:
        return
    try:
        os.killpg(os.getpgid(proc.pid), sig)
    except ProcessLookupError:
        return


def cleanup_sim_processes():
    subprocess.run(
        ["killall", "-9", "gzserver", "gzclient", "px4", "ruby", "MicroXRCEAgent"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )


def validate_tracking(csv_path, min_samples, max_abs_position_m, target_altitude_ned, max_mean_altitude_error_m):
    if not csv_path.exists():
        return False, "missing tracking CSV", {}

    df = pd.read_csv(csv_path)
    if len(df) < min_samples:
        return False, f"too few tracking samples ({len(df)} < {min_samples})", {"samples": len(df)}

    max_abs_position = float(df[["actual_x", "actual_y", "actual_z"]].abs().max().max())
    if max_abs_position > max_abs_position_m:
        return (
            False,
            f"invalid local-position magnitude ({max_abs_position:.2f} m > {max_abs_position_m:.2f} m)",
            {"samples": len(df), "max_abs_position_m": max_abs_position},
        )

    steady = df[df["t_s"] >= 25.0]
    if steady.empty:
        steady = df

    metrics = {
        "samples": int(len(df)),
        "duration_s": float(df["t_s"].max()),
        "mean_3d_error_m": float(steady["error_norm"].mean()),
        "rms_3d_error_m": float((steady["error_norm"] ** 2).mean() ** 0.5),
        "max_3d_error_m": float(steady["error_norm"].max()),
        "mean_xy_error_m": float((steady["error_x"] ** 2 + steady["error_y"] ** 2).pow(0.5).mean()),
        "mean_z_ned_m": float(steady["actual_z"].mean()),
        "max_abs_position_m": max_abs_position,
    }

    altitude_error = abs(metrics["mean_z_ned_m"] - target_altitude_ned)
    metrics["mean_altitude_error_m"] = altitude_error
    if altitude_error > max_mean_altitude_error_m:
        return (
            False,
            f"mean altitude error too large ({altitude_error:.2f} m > {max_mean_altitude_error_m:.2f} m)",
            metrics,
        )

    return (True, "valid tracking telemetry", metrics)


def summarize_swing(csv_path):
    if not csv_path.exists():
        return {"swing_valid": False, "swing_reason": "missing payload swing CSV"}

    df = pd.read_csv(csv_path)
    if df.empty:
        return {"swing_valid": False, "swing_reason": "empty payload swing CSV"}

    steady = df[df["t_s"] >= 25.0]
    if steady.empty:
        steady = df

    pose_source = steady["pose_source"].mode().iloc[0] if "pose_source" in steady and not steady.empty else "unknown"
    return {
        "swing_valid": True,
        "swing_reason": "valid payload swing telemetry",
        "swing_samples": int(len(df)),
        "pose_source": str(pose_source),
        "mean_cable_length_m": float(steady["cable_length_m"].mean()),
        "mean_lateral_swing_m": float(steady["lateral_swing_m"].mean()),
        "max_lateral_swing_m": float(steady["lateral_swing_m"].max()),
        "mean_cable_angle_deg": float(steady["cable_angle_deg"].mean()),
        "max_cable_angle_deg": float(steady["cable_angle_deg"].max()),
    }


def write_summary_md(out_dir, args, tracking_valid, tracking_reason, summary):
    lines = [
        "# Single Validation Run",
        "",
        f"**Created**: {datetime.now().isoformat(timespec='seconds')}",
        f"**Profile**: `{args.profile}`",
        f"**Launch File**: `{args.launch_file}`",
        f"**World**: `{args.world or 'none'}`",
        f"**Flight Duration**: `{args.flight_duration_s:.1f} s`",
        f"**Omega**: `{args.omega}`",
        f"**Hover Thrust**: `{args.hover_thrust}`",
        "",
        "## Result",
        "",
        f"- Tracking valid: `{tracking_valid}`",
        f"- Tracking reason: {tracking_reason}",
    ]

    if summary.get("swing_reason"):
        lines.append(f"- Payload swing reason: {summary['swing_reason']}")

    lines.extend(["", "## Metrics", ""])
    for key, value in summary.items():
        if isinstance(value, float):
            lines.append(f"- `{key}`: `{value:.4f}`")
        else:
            lines.append(f"- `{key}`: `{value}`")

    lines.extend(
        [
            "",
            "## Expected Plot Artifacts",
            "",
            "Generate these with `tools/plot_validation_run.py <run_dir>`:",
            "",
            "- `validation_xy_tracking.png`",
            "- `validation_3d_tracking.png`",
            "- `validation_xyz_vs_time.png`",
            "- `validation_error_swing.png`",
        ]
    )

    (out_dir / "VALIDATION_SUMMARY.md").write_text("\n".join(lines) + "\n")


def launch_file_for_profile(profile):
    if profile == "baseline":
        return "figure8_payload_experiment.launch.py"
    if profile == "hover":
        return "payload_hover_experiment.launch.py"
    return "geometric_figure8_experiment.launch.py"


def main():
    parser = argparse.ArgumentParser(description="Run one controlled PX4/ROS 2 payload validation trial.")
    parser.add_argument("--profile", choices=["geometric", "baseline", "hover"], default="geometric")
    parser.add_argument("--flight-duration-s", type=float, default=90.0)
    parser.add_argument("--sitl-startup-s", type=float, default=20.0)
    parser.add_argument("--omega", type=float, default=0.25)
    parser.add_argument("--hover-thrust", type=float, default=0.72)
    parser.add_argument("--min-samples", type=int, default=500)
    parser.add_argument("--max-abs-position-m", type=float, default=100.0)
    parser.add_argument("--target-altitude-ned", type=float, default=-5.0)
    parser.add_argument("--max-mean-altitude-error-m", type=float, default=1.0)
    parser.add_argument("--repo-root", default="~/uav-autonomous-telemetry")
    parser.add_argument("--px4-dir", default="~/PX4-Autopilot")
    parser.add_argument("--out-dir", default="")
    parser.add_argument("--gui", action="store_true", help="Open the Gazebo Classic client window during the run.")
    parser.add_argument(
        "--world",
        default="",
        help="Optional Gazebo Classic world name or absolute world path. Passed through PX4_SITL_WORLD.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).expanduser()
    px4_dir = Path(args.px4_dir).expanduser()
    args.launch_file = launch_file_for_profile(args.profile)

    if args.out_dir:
        out_dir = Path(args.out_dir).expanduser()
    else:
        stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        out_dir = repo_root / "reports" / f"single_validation_{stamp}_{args.profile}"
    logs_dir = out_dir / "logs"
    out_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    tracking_path = out_dir / "tracking_metrics.csv"
    swing_path = out_dir / "payload_swing_metrics.csv"

    cleanup_sim_processes()
    time.sleep(2)

    agent_log = (logs_dir / "microxrceagent.log").open("w")
    px4_log = (logs_dir / "px4_sitl.log").open("w")
    ros_log = (logs_dir / "ros2_launch.log").open("w")

    agent_proc = sitl_proc = ros_proc = None
    try:
        print("Starting MicroXRCEAgent...")
        agent_proc = subprocess.Popen(
            ["MicroXRCEAgent", "udp4", "-p", "8888"],
            stdout=agent_log,
            stderr=subprocess.STDOUT,
            preexec_fn=os.setsid,
        )
        time.sleep(2)

        print("Starting PX4 SITL...")
        headless_value = "0" if args.gui else "1"
        sitl_env = os.environ.copy()
        if args.world:
            sitl_env["PX4_SITL_WORLD"] = args.world
        sitl_proc = subprocess.Popen(
            ["make", "px4_sitl", "gazebo-classic_iris_depth_payload", f"HEADLESS={headless_value}"],
            cwd=px4_dir,
            env=sitl_env,
            stdout=px4_log,
            stderr=subprocess.STDOUT,
            preexec_fn=os.setsid,
        )
        time.sleep(args.sitl_startup_s)

        launch_args = [
            f"metrics_path:={tracking_path}",
            f"payload_metrics_path:={swing_path}",
        ]
        if args.profile in {"geometric", "baseline"}:
            launch_args.append(f"omega:={args.omega}")
        if args.profile == "geometric":
            launch_args.append(f"hover_thrust:={args.hover_thrust}")

        ros_cmd = (
            "source /opt/ros/humble/setup.bash && "
            "source ~/px4_msgs_ws/install/setup.bash && "
            "source ~/uav-autonomous-telemetry/ros2_ws/install/setup.bash && "
            f"ros2 launch uav_control {args.launch_file} "
            + " ".join(launch_args)
        )
        print("Starting ROS 2 validation launch...")
        ros_proc = subprocess.Popen(
            ["bash", "-lc", ros_cmd],
            cwd=repo_root,
            stdout=ros_log,
            stderr=subprocess.STDOUT,
            preexec_fn=os.setsid,
        )

        print(f"Flying for {args.flight_duration_s:.1f} seconds...")
        time.sleep(args.flight_duration_s)
    finally:
        print("Stopping validation processes...")
        terminate_process(ros_proc)
        time.sleep(2)
        terminate_process(sitl_proc)
        time.sleep(2)
        terminate_process(agent_proc)
        time.sleep(3)
        cleanup_sim_processes()
        agent_log.close()
        px4_log.close()
        ros_log.close()

    tracking_valid, tracking_reason, summary = validate_tracking(
        tracking_path,
        min_samples=args.min_samples,
        max_abs_position_m=args.max_abs_position_m,
        target_altitude_ned=args.target_altitude_ned,
        max_mean_altitude_error_m=args.max_mean_altitude_error_m,
    )
    summary.update(summarize_swing(swing_path))
    summary.update(
        {
            "profile": args.profile,
            "launch_file": args.launch_file,
            "world": args.world or "none",
            "tracking_valid": tracking_valid,
            "tracking_reason": tracking_reason,
            "output_dir": str(out_dir),
        }
    )

    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    write_summary_md(out_dir, args, tracking_valid, tracking_reason, summary)

    print(json.dumps(summary, indent=2))
    print(f"Validation artifacts written to {out_dir}")


if __name__ == "__main__":
    main()
