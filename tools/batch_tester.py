#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import shutil
import pandas as pd
from pathlib import Path

NUM_RUNS = 50
FLIGHT_DURATION = 150 # seconds

def run_single_trial(trial_idx, out_dir):
    print(f"\n--- Starting Trial {trial_idx}/{NUM_RUNS} ---")
    px4_dir = os.path.expanduser("~/PX4-Autopilot")
    
    # 1. Start SITL
    sitl_proc = subprocess.Popen(
        ["make", "px4_sitl", "gazebo-classic_iris_depth_payload", "HEADLESS=1"],
        cwd=px4_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid
    )
    time.sleep(15)
    
    # 2. Start ROS 2 Launch
    ros_cmd = "source /opt/ros/humble/setup.bash && source ~/px4_msgs_ws/install/setup.bash && source ~/uav-autonomous-telemetry/ros2_ws/install/setup.bash && ros2 launch uav_control geometric_figure8_experiment.launch.py"
    ros_proc = subprocess.Popen(
        ["bash", "-c", ros_cmd],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid
    )
    
    # 3. Wait for flight
    time.sleep(FLIGHT_DURATION)
    
    # 4. Clean up
    os.killpg(os.getpgid(ros_proc.pid), 2)
    os.killpg(os.getpgid(sitl_proc.pid), 2)
    time.sleep(5)
    subprocess.run(["killall", "-9", "gzserver", "gzclient", "px4", "ruby"], stderr=subprocess.DEVNULL)
    
    # 5. Check Success and Move Files
    repo_root = Path("~/uav-autonomous-telemetry").expanduser()
    trial_out = out_dir / f"trial_{trial_idx:02d}"
    trial_out.mkdir(parents=True, exist_ok=True)
    
    success = False
    try:
        shutil.copy(repo_root / "figure8_tracking_metrics.csv", trial_out / "figure8_tracking_metrics.csv")
        shutil.copy(repo_root / "payload_swing_metrics.csv", trial_out / "payload_swing_metrics.csv")
        
        # Verify success by checking if the flight completed enough points (basic check)
        df = pd.read_csv(trial_out / "figure8_tracking_metrics.csv")
        if len(df) > 1000:  # Assuming 50Hz for 150s = 7500 points
            success = True
            
        # Clean up root files for next trial
        os.remove(repo_root / "figure8_tracking_metrics.csv")
        os.remove(repo_root / "payload_swing_metrics.csv")
    except FileNotFoundError:
        pass
    
    status = "SUCCESS" if success else "FAILURE"
    print(f"Trial {trial_idx} completed with status: {status}")
    return success

def main():
    repo_root = Path("~/uav-autonomous-telemetry").expanduser()
    batch_dir = repo_root / "reports/batch_testing"
    batch_dir.mkdir(parents=True, exist_ok=True)
    
    results = []
    
    for i in range(1, NUM_RUNS + 1):
        success = run_single_trial(i, batch_dir)
        results.append({
            'trial': i,
            'success': success
        })
        
        # Save running results
        df = pd.DataFrame(results)
        df.to_csv(batch_dir / "batch_results_summary.csv", index=False)
        
    # Final summary
    df = pd.DataFrame(results)
    success_rate = df['success'].mean() * 100.0
    print(f"\n====================================")
    print(f"Batch Testing Complete!")
    print(f"Total Runs: {NUM_RUNS}")
    print(f"Success Rate: {success_rate:.2f}%")
    print(f"====================================")
    
    with open(batch_dir / "summary.txt", "w") as f:
        f.write(f"Batch Testing Complete!\n")
        f.write(f"Total Runs: {NUM_RUNS}\n")
        f.write(f"Success Rate: {success_rate:.2f}%\n")

if __name__ == "__main__":
    main()
