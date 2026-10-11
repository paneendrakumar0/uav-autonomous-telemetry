#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# UAV Slung-Payload Automated Reference Test
# ---------------------------------------------------------------------------
# A highly robust, configurable execution script that spins up the SITL
# environment, runs the Figure-8 trajectory, and validates performance.

set -euo pipefail

# --- Configuration & Defaults ---
OMEGA=0.25
THRESHOLD=0.50
STEADY_STATE_START=25.0
DURATION=50
WORKSPACE_DIR=$(pwd)
PX4_DIR=${PX4_DIR:-$HOME/PX4-Autopilot}

# Generate timestamped report directory to prevent overwriting past experiments
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORTS_DIR="$WORKSPACE_DIR/reports/reference_test_$TIMESTAMP"
METRICS_FILE="$REPORTS_DIR/figure8_tracking_metrics.csv"

# --- UI Formatting ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

log_info()    { echo -e "${CYAN}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_err()     { echo -e "${RED}[ERROR]${NC} $1"; }

# --- CLI Parsing ---
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -w|--omega) OMEGA="$2"; shift ;;
        -t|--threshold) THRESHOLD="$2"; shift ;;
        -d|--duration) DURATION="$2"; shift ;;
        -h|--help)
            echo -e "Usage: $0 [options]\n"
            echo "Options:"
            echo "  -w, --omega <float>       Trajectory angular rate (default: 0.25)"
            echo "  -t, --threshold <float>   Pass/Fail error threshold in meters (default: 0.50)"
            echo "  -d, --duration <int>      Experiment duration in seconds (default: 50)"
            exit 0
            ;;
        *) log_err "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# --- Pre-flight Checks ---
log_info "Running pre-flight environment checks..."
if ! command -v MicroXRCEAgent &> /dev/null; then
    log_err "MicroXRCEAgent not found. Ensure it is installed and in your PATH."
    exit 1
fi
if [[ ! -d "$PX4_DIR" ]]; then
    log_err "PX4 directory not found at $PX4_DIR. Set PX4_DIR environment variable."
    exit 1
fi
if ! python3 -c "import pandas" &> /dev/null; then
    log_err "Python pandas library is missing. Run: pip3 install pandas"
    exit 1
fi

mkdir -p "$REPORTS_DIR"
log_success "Environment verified. Logs will be saved to: $REPORTS_DIR"

# --- Process Management ---
declare -a PIDS

cleanup() {
    echo ""
    log_info "Initiating graceful teardown of background processes..."
    for pid in "${PIDS[@]}"; do
        kill -INT "$pid" 2>/dev/null || true
    done
    # Failsafe kill for detached SITL processes
    pkill -f gzserver 2>/dev/null || true
    pkill -f px4 2>/dev/null || true
    log_success "Teardown complete."
}
trap cleanup EXIT

# --- Execution ---
log_info "Starting Micro XRCE-DDS Agent..."
MicroXRCEAgent udp4 -p 8888 > "$REPORTS_DIR/xrce.log" 2>&1 &
PIDS+=($!)
sleep 2

log_info "Starting PX4 SITL (Headless Gazebo Classic)..."
pushd "$PX4_DIR" > /dev/null
HEADLESS=1 make px4_sitl gazebo-classic_iris_depth_camera > "$REPORTS_DIR/px4.log" 2>&1 &
PIDS+=($!)
popd > /dev/null

log_info "Waiting for PX4 & Gazebo to initialize..."
sleep 15

log_info "Launching ROS 2 offboard controller (omega=${OMEGA} rad/s)..."
pushd "$WORKSPACE_DIR/ros2_ws" > /dev/null
# Source environment safely
[[ -f /opt/ros/humble/setup.bash ]] && source /opt/ros/humble/setup.bash
[[ -f install/setup.bash ]] && source install/setup.bash

ros2 launch uav_control figure8_experiment.launch.py \
    metrics_path:="$METRICS_FILE" \
    omega:="$OMEGA" > "$REPORTS_DIR/ros2.log" 2>&1 &
PIDS+=($!)
popd > /dev/null

# --- Flight Monitoring ---
echo -n -e "${CYAN}[INFO]${NC} Flying reference trajectory. Collecting data for ${DURATION}s "
for ((i=1; i<=DURATION; i++)); do
    sleep 1
    echo -n "."
done
echo " Done."

# --- Analysis ---
echo "--------------------------------------------------------"
log_info "Evaluating Flight Metrics..."
echo "--------------------------------------------------------"

if [[ ! -f "$METRICS_FILE" ]]; then
    log_err "Metrics CSV was not generated. Check $REPORTS_DIR for crash logs."
    exit 1
fi

python3 "$WORKSPACE_DIR/tools/evaluate_reference_metrics.py" \
    --csv "$METRICS_FILE" \
    --threshold "$THRESHOLD" \
    --steady-start "$STEADY_STATE_START"
