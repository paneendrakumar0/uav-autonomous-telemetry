#!/usr/bin/env python3
import os
import subprocess
import time
import signal
from pathlib import Path

def main():
    print("Starting Task 1: Media Capture...")
    repo_root = Path(__file__).resolve().parent.parent
    media_dir = repo_root / "reports/media"
    media_dir.mkdir(parents=True, exist_ok=True)
    
    display = os.environ.get("DISPLAY", ":1")
    
    # 1. Start PX4 SITL + Gazebo GUI
    print("Launching PX4 SITL and Gazebo...")
    px4_dir = os.path.expanduser("~/PX4-Autopilot")
    sitl_proc = subprocess.Popen(
        ["make", "px4_sitl", "gazebo-classic_iris_depth_payload"],
        cwd=px4_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid
    )
    
    time.sleep(20) # Wait for Gazebo GUI to fully load
    
    # 2. Takeoff screenshot
    print("Taking takeoff screenshot...")
    subprocess.run(["import", "-window", "root", str(media_dir / "takeoff.png")])
    
    # 3. Start ffmpeg recording
    print("Starting ffmpeg screen recording...")
    # Using 2560x1600 as detected previously, but -video_size can be omitted if we just capture the whole screen? No, x11grab requires it.
    # Actually, we can use `xdpyinfo | grep dimensions` to get the exact size, but 2560x1600 works.
    ffmpeg_proc = subprocess.Popen(
        ["ffmpeg", "-y", "-video_size", "2560x1600", "-framerate", "25", "-f", "x11grab", "-i", f"{display}.0+0,0", str(media_dir / "flight_sequence.mp4")],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    # 4. Launch ROS 2 node
    print("Launching ROS 2 controller...")
    ros_env = os.environ.copy()
    # Source workspaces using bash
    ros_cmd = "source /opt/ros/humble/setup.bash && source ~/px4_msgs_ws/install/setup.bash && source ~/uav-autonomous-telemetry/ros2_ws/install/setup.bash && ros2 launch uav_control geometric_figure8_experiment.launch.py"
    ros_proc = subprocess.Popen(
        ["bash", "-c", ros_cmd],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid
    )
    
    time.sleep(40) # Wait until steady state figure-8
    
    # 5. Steady state screenshot
    print("Taking steady state screenshot...")
    subprocess.run(["import", "-window", "root", str(media_dir / "steady_state.png")])
    
    print("Waiting for flight completion...")
    time.sleep(110) # 40 + 110 = 150s total flight time
    
    # 6. Landing screenshot
    print("Taking landing screenshot...")
    subprocess.run(["import", "-window", "root", str(media_dir / "landing.png")])
    
    # 7. Stop recording gracefully
    print("Stopping recording...")
    ffmpeg_proc.send_signal(signal.SIGINT)
    ffmpeg_proc.wait(timeout=10)
    
    # 8. Teardown
    print("Tearing down simulation...")
    os.killpg(os.getpgid(ros_proc.pid), signal.SIGINT)
    os.killpg(os.getpgid(sitl_proc.pid), signal.SIGINT)
    
    time.sleep(5)
    subprocess.run(["killall", "-9", "gzserver", "gzclient", "px4", "ruby"], stderr=subprocess.DEVNULL)
    print("Task 1 complete!")

if __name__ == "__main__":
    main()
