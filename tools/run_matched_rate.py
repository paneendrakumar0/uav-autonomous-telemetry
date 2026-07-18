#!/usr/bin/env python3
import os
import subprocess
import time
import shutil
from pathlib import Path

def run_experiment(launch_file, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Starting SITL for {launch_file}...")
    px4_dir = os.path.expanduser("~/PX4-Autopilot")
    sitl_proc = subprocess.Popen(
        ["make", "px4_sitl", "gazebo-classic_iris_depth_payload", "HEADLESS=1"],
        cwd=px4_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid
    )
    time.sleep(15)
    
    print("Launching ROS 2 nodes...")
    ros_cmd = f"source /opt/ros/humble/setup.bash && source ~/px4_msgs_ws/install/setup.bash && source ~/uav-autonomous-telemetry/ros2_ws/install/setup.bash && ros2 launch uav_control {launch_file}"
    ros_proc = subprocess.Popen(
        ["bash", "-c", ros_cmd],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid
    )
    
    print("Waiting 150 seconds for flight to complete...")
    for i in range(150, 0, -10):
        print(f"... {i}s remaining")
        time.sleep(10)
        
    print("Killing processes...")
    os.killpg(os.getpgid(ros_proc.pid), 2)
    os.killpg(os.getpgid(sitl_proc.pid), 2)
    time.sleep(5)
    subprocess.run(["killall", "-9", "gzserver", "gzclient", "px4", "ruby"], stderr=subprocess.DEVNULL)
    
    # Copy files
    repo_root = Path("~/uav-autonomous-telemetry").expanduser()
    try:
        shutil.copy(repo_root / "figure8_tracking_metrics.csv", out_dir / "figure8_tracking_metrics.csv")
        print(f"Copied tracking metrics to {out_dir}")
    except FileNotFoundError:
        pass
    
    try:
        shutil.copy(repo_root / "payload_swing_metrics.csv", out_dir / "payload_swing_metrics.csv")
        print(f"Copied swing metrics to {out_dir}")
    except FileNotFoundError:
        pass
    print(f"Finished {launch_file}\n")


def main():
    repo_root = Path("~/uav-autonomous-telemetry").expanduser()
    matched_rate_dir = repo_root / "reports/matched_rate"
    
    # 1. Baseline Run
    run_experiment("figure8_payload_experiment.launch.py", matched_rate_dir / "baseline")
    
    # 2. Geometric Run
    # Note: geometric_figure8_experiment defaults to omega=0.25 and fig8_ramp_s=5.0
    run_experiment("geometric_figure8_experiment.launch.py", matched_rate_dir / "geometric")

    print("Running plot comparison...")
    subprocess.run([
        "python3", "tools/plot_comparison.py",
        "--baseline_csv", str(matched_rate_dir / "baseline" / "figure8_tracking_metrics.csv"),
        "--geometric_csv", str(matched_rate_dir / "geometric" / "figure8_tracking_metrics.csv"),
        "--baseline_swing", str(matched_rate_dir / "baseline" / "payload_swing_metrics.csv"),
        "--geometric_swing", str(matched_rate_dir / "geometric" / "payload_swing_metrics.csv"),
        "--out_dir", str(matched_rate_dir)
    ])

if __name__ == "__main__":
    main()
