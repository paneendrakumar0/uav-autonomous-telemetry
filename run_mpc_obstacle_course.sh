#!/bin/bash
set -e

echo "=========================================================="
echo " UAV Slung-Payload Autonomous Obstacle Avoidance Run "
echo "=========================================================="

WORKSPACE_DIR=$(pwd)
PX4_DIR=${PX4_DIR:-$HOME/PX4-Autopilot}
REPORTS_DIR="$WORKSPACE_DIR/reports/obstacle_avoidance_run"
METRICS_FILE="$REPORTS_DIR/obstacle_traversal_metrics.csv"

mkdir -p "$REPORTS_DIR"
rm -f "$METRICS_FILE"

echo "[1/4] Starting Micro XRCE-DDS Agent..."
MicroXRCEAgent udp4 -p 8888 > "$REPORTS_DIR/xrce.log" 2>&1 &
XRCE_PID=$!
sleep 2

echo "[2/4] Starting PX4 SITL + Gazebo Classic (Obstacle Course World)..."
if [ ! -d "$PX4_DIR" ]; then
    echo "Error: PX4 directory not found at $PX4_DIR"
    kill $XRCE_PID
    exit 1
fi

cd "$PX4_DIR"
export PX4_SITL_WORLD=payload_obstacle_course
HEADLESS=1 make px4_sitl gazebo-classic_iris_depth_payload > "$REPORTS_DIR/px4.log" 2>&1 &
PX4_PID=$!
sleep 60

echo "[3/4] Launching OctoMap 3D Mapping & Payload-Aware MPC..."
cd "$WORKSPACE_DIR/ros2_ws"
[ -f /opt/ros/humble/setup.bash ] && source /opt/ros/humble/setup.bash
[ -f "$HOME/px4_msgs_ws/install/setup.bash" ] && source "$HOME/px4_msgs_ws/install/setup.bash"
[ -f install/setup.bash ] && source install/setup.bash

ros2 launch uav_control mpc_obstacle_avoidance.launch.py metrics_path:="$METRICS_FILE" > "$REPORTS_DIR/ros2.log" 2>&1 &
ROS_PID=$!

echo "Waiting 65 seconds for drone to traverse the obstacle course..."
sleep 65

echo "[4/4] Cleaning up simulation processes..."
kill -INT $ROS_PID 2>/dev/null || true
sleep 2
kill -INT $PX4_PID 2>/dev/null || true
kill -INT $XRCE_PID 2>/dev/null || true
pkill -f gazebo || true
pkill -f gzserver || true
pkill -f px4 || true
sleep 2

echo "=========================================================="
echo " Analyzing Obstacle Avoidance & Swing Metrics "
echo "=========================================================="

if [ ! -f "$METRICS_FILE" ]; then
    echo -e "\e[31m[FAIL]\e[0m Metrics CSV was not generated. Check logs in $REPORTS_DIR"
    exit 1
fi

python3 "$WORKSPACE_DIR/tools/evaluate_obstacle_metrics.py" --csv "$METRICS_FILE"

echo "=========================================================="
echo " Rendering 3D Screen Recording & Video Artifacts "
echo "=========================================================="
if [ -f "$WORKSPACE_DIR/.venv/bin/python" ]; then
    "$WORKSPACE_DIR/.venv/bin/python" "$WORKSPACE_DIR/tools/render_obstacle_animation.py" \
        --csv "$METRICS_FILE" \
        --mp4 "$REPORTS_DIR/obstacle_avoidance_flight.mp4" \
        --gif "$REPORTS_DIR/obstacle_avoidance_flight.gif"
else
    python3 "$WORKSPACE_DIR/tools/render_obstacle_animation.py" \
        --csv "$METRICS_FILE" \
        --mp4 "$REPORTS_DIR/obstacle_avoidance_flight.mp4" \
        --gif "$REPORTS_DIR/obstacle_avoidance_flight.gif"
fi
