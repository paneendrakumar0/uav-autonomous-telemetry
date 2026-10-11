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

echo "Waiting 20 seconds for the Gazebo GUI window to load..."
sleep 20

echo "=========================================================="
echo " Launching Payload-Aware Convex MPC Obstacle Flight...   "
echo "=========================================================="
cd "$WORKSPACE_DIR/ros2_ws"
[ -f /opt/ros/humble/setup.bash ] && source /opt/ros/humble/setup.bash
[ -f "$HOME/px4_msgs_ws/install/setup.bash" ] && source "$HOME/px4_msgs_ws/install/setup.bash"
[ -f install/setup.bash ] && source install/setup.bash

ros2 launch uav_control mpc_obstacle_avoidance.launch.py metrics_path:="$METRICS_FILE" &
ROS_PID=$!

cleanup() {
    echo ""
    echo "Shutting down simulation..."
    kill -INT $ROS_PID 2>/dev/null || true
    kill -INT $PX4_PID 2>/dev/null || true
    kill -INT $XRCE_PID 2>/dev/null || true
    pkill -f gzclient 2>/dev/null || true
    pkill -f gzserver 2>/dev/null || true
    pkill -f px4 2>/dev/null || true
    echo "Shutdown complete."
}
trap cleanup EXIT INT TERM

echo ""
echo "=========================================================="
echo " THE DRONE IS NOW FLYING IN THE 3D GAZEBO WINDOW!        "
echo " You can now record your screen or the Gazebo window.    "
echo " Press Ctrl+C in this terminal when you want to stop.    "
echo "=========================================================="
echo ""

wait $ROS_PID 2>/dev/null || true
