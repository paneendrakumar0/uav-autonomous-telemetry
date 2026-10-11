#!/bin/bash
# ==============================================================================
# UAV Slung-Payload Autonomous Obstacle Avoidance - Live 3D GUI Run
# ==============================================================================
# This script launches Gazebo Classic WITH ITS 3D GRAPHICAL USER INTERFACE
# on your screen so you can watch and screen-record the vehicle in real-time.

set -e

WORKSPACE_DIR=$(pwd)
PX4_DIR=${PX4_DIR:-$HOME/PX4-Autopilot}
REPORTS_DIR="$WORKSPACE_DIR/reports/obstacle_avoidance_run"
METRICS_FILE="$REPORTS_DIR/obstacle_traversal_metrics.csv"

mkdir -p "$REPORTS_DIR"

echo "=========================================================="
echo " Starting Micro XRCE-DDS Agent..."
echo "=========================================================="
MicroXRCEAgent udp4 -p 8888 > "$REPORTS_DIR/xrce.log" 2>&1 &
XRCE_PID=$!
sleep 2

echo "=========================================================="
echo " Starting Gazebo Classic 3D GUI Window on your desktop..."
echo " (Loading payload_obstacle_course.world with 3D models)  "
echo "=========================================================="
cd "$PX4_DIR"
export PX4_SITL_WORLD=payload_obstacle_course
# NOTICE: We deliberately omit HEADLESS=1 so the 3D window pops up on your screen!
make px4_sitl gazebo-classic_iris_depth_payload > "$REPORTS_DIR/px4.log" 2>&1 &
PX4_PID=$!

echo "Waiting for Gazebo 3D simulation window to appear on screen..."
for i in $(seq 1 60); do
    if pgrep -f gzclient >/dev/null && pgrep -f gzserver >/dev/null; then
        echo "Gazebo GUI window is open and connected to simulation!"
        break
    fi
    sleep 1
done

# Allow Gazebo scene and models to settle
sleep 3

cleanup() {
    echo ""
    echo "Shutting down simulation..."
    kill -INT $ROS_PID 2>/dev/null || true
    kill -INT $PX4_PID 2>/dev/null || true
    kill -INT $XRCE_PID 2>/dev/null || true
    pkill -f gzclient 2>/dev/null || true
    pkill -f gzserver 2>/dev/null || true
    pkill -f px4 2>/dev/null || true
    echo "Simulation shutdown complete."
}
trap cleanup EXIT INT TERM

echo "=========================================================="
echo " Launching Payload-Aware Convex MPC Obstacle Flight...   "
echo "=========================================================="
cd "$WORKSPACE_DIR/ros2_ws"
[ -f /opt/ros/humble/setup.bash ] && source /opt/ros/humble/setup.bash
[ -f "$HOME/px4_msgs_ws/install/setup.bash" ] && source "$HOME/px4_msgs_ws/install/setup.bash"
[ -f install/setup.bash ] && source install/setup.bash

echo ""
echo "=========================================================="
echo " THE DRONE IS NOW FLYING IN THE 3D GAZEBO WINDOW!        "
echo " You can now record your screen or the Gazebo window.    "
echo " Trajectory will automatically complete at the goal.     "
echo " Press Ctrl+C anytime if you want to abort early.        "
echo "=========================================================="
echo ""

ros2 launch uav_control mpc_obstacle_avoidance.launch.py metrics_path:="$METRICS_FILE" &
ROS_PID=$!

wait $ROS_PID 2>/dev/null || true

echo "=========================================================="
echo " Analyzing Obstacle Avoidance & Swing Metrics "
echo "=========================================================="

if [ -f "$METRICS_FILE" ]; then
    python3 "$WORKSPACE_DIR/tools/evaluate_obstacle_metrics.py" --csv "$METRICS_FILE"
fi
