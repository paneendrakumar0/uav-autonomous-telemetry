#!/usr/bin/env bash
# run_reference_experiment.sh
# Automates the baseline Figure-8 reference experiment and evaluates tracking performance.

set -e

WORKSPACE_DIR=$(pwd)
PX4_DIR=${PX4_DIR:-$HOME/PX4-Autopilot}
REPORTS_DIR="$WORKSPACE_DIR/reports/reference_test"
METRICS_FILE="$REPORTS_DIR/figure8_tracking_metrics.csv"

mkdir -p "$REPORTS_DIR"
rm -f "$METRICS_FILE"

# Track background process PIDs for clean teardown
declare -a PIDS

cleanup() {
    echo -e "\nCleaning up background processes..."
    for pid in "${PIDS[@]}"; do
        kill -INT "$pid" 2>/dev/null || true
    done
    # Catch-all for simulator processes if they detach
    pkill -f gzserver 2>/dev/null || true
    pkill -f px4 2>/dev/null || true
    echo "Cleanup complete."
}
trap cleanup EXIT

echo "[1/3] Starting Micro XRCE-DDS Agent..."
MicroXRCEAgent udp4 -p 8888 > "$REPORTS_DIR/xrce.log" 2>&1 &
PIDS+=($!)
sleep 2

echo "[2/3] Starting PX4 SITL (gazebo-classic_iris_depth_camera)..."
if [ ! -d "$PX4_DIR" ]; then
    echo "Error: PX4 directory not found at $PX4_DIR."
    echo "Please set the PX4_DIR environment variable."
    exit 1
fi

pushd "$PX4_DIR" > /dev/null
HEADLESS=1 make px4_sitl gazebo-classic_iris_depth_camera > "$REPORTS_DIR/px4.log" 2>&1 &
PIDS+=($!)
popd > /dev/null

# Wait for Gazebo and PX4 to fully initialize
sleep 15

echo "[3/3] Launching ROS 2 offboard controller (omega=0.25)..."
pushd "$WORKSPACE_DIR/ros2_ws" > /dev/null
# Source environment layers safely
[ -f /opt/ros/humble/setup.bash ] && source /opt/ros/humble/setup.bash
[ -f install/setup.bash ] && source install/setup.bash

ros2 launch uav_control figure8_experiment.launch.py \
    metrics_path:="$METRICS_FILE" \
    omega:=0.25 > "$REPORTS_DIR/ros2.log" 2>&1 &
PIDS+=($!)
popd > /dev/null

echo "Experiment running. Waiting 50 seconds to collect steady-state data..."
sleep 50

echo "------------------------------------------------"
echo "Evaluating Metrics"
echo "------------------------------------------------"
python3 "$WORKSPACE_DIR/tools/evaluate_reference_metrics.py" "$METRICS_FILE"
