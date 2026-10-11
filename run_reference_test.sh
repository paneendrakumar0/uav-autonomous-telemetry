#!/bin/bash
set -e

echo "=========================================="
echo " UAV Slung-Payload Automated Reference Test "
echo "=========================================="

WORKSPACE_DIR=$(pwd)
PX4_DIR=${PX4_DIR:-$HOME/PX4-Autopilot}
REPORTS_DIR="$WORKSPACE_DIR/reports/reference_test"
METRICS_FILE="$REPORTS_DIR/figure8_tracking_metrics.csv"

mkdir -p "$REPORTS_DIR"
rm -f "$METRICS_FILE"

echo "[1/4] Starting Micro XRCE-DDS Agent..."
MicroXRCEAgent udp4 -p 8888 > "$REPORTS_DIR/xrce.log" 2>&1 &
XRCE_PID=$!
sleep 2

echo "[2/4] Starting PX4 SITL (Headless)..."
if [ ! -d "$PX4_DIR" ]; then
    echo "Error: PX4 directory not found at $PX4_DIR"
    echo "Please set PX4_DIR environment variable if it's installed elsewhere."
    kill $XRCE_PID
    exit 1
fi
cd "$PX4_DIR"
HEADLESS=1 make px4_sitl gazebo-classic_iris_depth_payload > "$REPORTS_DIR/px4.log" 2>&1 &
PX4_PID=$!
sleep 60

echo "[3/4] Launching ROS 2 offboard control (omega=0.25)..."
cd "$WORKSPACE_DIR/ros2_ws"
# Source ROS 2 and workspace layers if available
[ -f /opt/ros/humble/setup.bash ] && source /opt/ros/humble/setup.bash
[ -f "$HOME/px4_msgs_ws/install/setup.bash" ] && source "$HOME/px4_msgs_ws/install/setup.bash"
[ -f install/setup.bash ] && source install/setup.bash

ros2 launch uav_control geometric_figure8_experiment.launch.py metrics_path:="$METRICS_FILE" omega:=0.25 hover_thrust:=0.72 > "$REPORTS_DIR/ros2.log" 2>&1 &
ROS_PID=$!

# The script collects steady-state data post-25s. 85 seconds allows takeoff + full trajectory.
echo "Waiting 85 seconds for experiment to collect steady-state data..."
sleep 85

echo "[4/4] Cleaning up processes..."
kill -INT $ROS_PID 2>/dev/null || true
sleep 2
kill -INT $PX4_PID 2>/dev/null || true
kill -INT $XRCE_PID 2>/dev/null || true
pkill -f gazebo || true
pkill -f gzserver || true
pkill -f px4 || true
sleep 2

echo "=========================================="
echo " Analyzing Metrics "
echo "=========================================="

if [ ! -f "$METRICS_FILE" ]; then
    echo -e "\e[31m[FAIL]\e[0m Metrics CSV was not generated. Check logs in $REPORTS_DIR"
    exit 1
fi

python3 "$WORKSPACE_DIR/tools/evaluate_reference_metrics.py" --csv "$METRICS_FILE" --threshold 0.50 --steady-start 25.0
