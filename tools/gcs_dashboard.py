#!/usr/bin/env python3
import sys
import os
import signal
import subprocess
import time
import math
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QComboBox, QGroupBox, QGridLayout
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QFont

# Pyqtgraph for telemetry
import pyqtgraph as pg

import rclpy
from rclpy.node import Node
from px4_msgs.msg import VehicleOdometry

# ==============================================================================
# Phase 1: Subprocess Manager (The Execution Engine)
# ==============================================================================
class SubprocessManager:
    """Safely spins up and tears down bash commands and background processes."""
    def __init__(self):
        self.processes = []

    def launch(self, cmd, cwd=None):
        print(f"[GCS] Launching: {cmd}")
        p = subprocess.Popen(
            cmd, shell=True, cwd=cwd,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid
        )
        self.processes.append(p)
        return p

    def kill_all(self):
        print("[GCS] Initiating emergency teardown...")
        for p in self.processes:
            try:
                os.killpg(os.getpgid(p.pid), signal.SIGTERM)
            except ProcessLookupError:
                pass
        self.processes.clear()
        subprocess.run("pkill -9 px4 2>/dev/null", shell=True)
        subprocess.run("pkill -9 gzserver 2>/dev/null", shell=True)
        subprocess.run("pkill -9 gzclient 2>/dev/null", shell=True)
        print("[GCS] Teardown complete. All processes killed.")

# ==============================================================================
# Phase 1 & 3: ROS 2 Worker Thread
# ==============================================================================
class ROS2Worker(QThread):
    """Runs rclpy.spin() in the background to prevent GUI freezing."""
    log_signal = pyqtSignal(str)
    telemetry_signal = pyqtSignal(float, float) # time, altitude

    def __init__(self):
        super().__init__()
        self.node = None
        self.start_time = time.time()

    def run(self):
        rclpy.init()
        self.node = rclpy.create_node('gcs_telemetry_listener')
        
        # Phase 3: Telemetry Subscriptions
        self.odom_sub = self.node.create_subscription(
            VehicleOdometry,
            '/fmu/out/vehicle_odometry',
            self.odom_callback,
            10
        )
        
        self.log_signal.emit("ROS 2 Telemetry Node Initialized. Subscribed to Odometry.")
        rclpy.spin(self.node)
        
    def odom_callback(self, msg):
        # PX4 uses NED frame, so -Z is Altitude (Up)
        t = time.time() - self.start_time
        alt = -msg.position[2]
        if math.isfinite(alt):
            self.telemetry_signal.emit(t, alt)

    def stop(self):
        if self.node:
            self.node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
        self.quit()
        self.wait()

# ==============================================================================
# Phase 1, 2 & 3: Main Ground Control Station Window
# ==============================================================================
class GroundControlStation(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UAV Autonomous Telemetry - Ground Control Station")
        self.resize(1000, 700)

        self.proc_manager = SubprocessManager()
        
        # Phase 3: Telemetry Data Buffers
        self.time_data = []
        self.alt_data = []
        
        self.init_ui()

        # Start ROS 2 Worker Thread
        self.ros_worker = ROS2Worker()
        self.ros_worker.log_signal.connect(self.update_log)
        self.ros_worker.telemetry_signal.connect(self.update_telemetry)
        self.ros_worker.start()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Main Grid Layout
        grid = QGridLayout(main_widget)
        
        # Header
        header = QLabel("GROUND CONTROL STATION - UAV SLUNG PAYLOAD")
        header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("color: #ecf0f1; background-color: #34495e; padding: 10px;")
        grid.addWidget(header, 0, 0, 1, 2)

        # Panel 1: Mission Command Deck
        cmd_group = QGroupBox("Mission Command Deck")
        cmd_group.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid #7f8c8d; margin-top: 10px; }")
        cmd_layout = QVBoxLayout()

        self.mission_selector = QComboBox()
        self.mission_selector.addItems([
            "Phase 1: Figure-8 Baseline (Empty World)",
            "Phase 2: MPC Obstacle Avoidance (Cluttered World)"
        ])
        self.mission_selector.setStyleSheet("padding: 5px; font-size: 14px;")
        cmd_layout.addWidget(QLabel("Select Flight Regime:"))
        cmd_layout.addWidget(self.mission_selector)

        # Launch/Kill Matrix
        btn_layout = QHBoxLayout()
        self.btn_launch = QPushButton("🚀 LAUNCH SIMULATION")
        self.btn_launch.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 15px;")
        self.btn_launch.clicked.connect(self.launch_sim)
        
        self.btn_kill = QPushButton("🛑 ABORT / KILL ALL")
        self.btn_kill.setStyleSheet("background-color: #c0392b; color: white; font-weight: bold; padding: 15px;")
        self.btn_kill.clicked.connect(self.kill_sim)
        
        btn_layout.addWidget(self.btn_launch)
        btn_layout.addWidget(self.btn_kill)
        cmd_layout.addLayout(btn_layout)
        cmd_group.setLayout(cmd_layout)
        grid.addWidget(cmd_group, 1, 0, 1, 2)

        # Panel 2: Phase 3 Telemetry Oscilloscopes
        self.telemetry_group = QGroupBox("Live Telemetry Stream: Drone Altitude")
        self.telemetry_group.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid #7f8c8d; margin-top: 10px; }")
        tel_layout = QVBoxLayout()
        
        # Setup PyQtGraph
        pg.setConfigOptions(antialias=True)
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('#1e1e1e')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.plot_widget.setLabel('left', 'Altitude', units='meters')
        self.plot_widget.setLabel('bottom', 'Time', units='seconds')
        self.alt_curve = self.plot_widget.plot(pen=pg.mkPen('#00d2d3', width=3))
        
        tel_layout.addWidget(self.plot_widget)
        self.telemetry_group.setLayout(tel_layout)
        grid.addWidget(self.telemetry_group, 2, 0, 1, 1)

        # Panel 3: Perception Suite (Placeholder for Phase 4)
        self.vision_group = QGroupBox("Perception Suite")
        self.vision_group.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid #7f8c8d; margin-top: 10px; }")
        vis_layout = QVBoxLayout()
        vis_layout.addWidget(QLabel("[Phase 4: FPV Video & RViz 3D Map will dock here]"))
        self.vision_group.setLayout(vis_layout)
        grid.addWidget(self.vision_group, 2, 1, 1, 1)

        # Status Log
        self.status_log = QLabel("System Ready. Select a mission and Launch...")
        self.status_log.setStyleSheet("background-color: #2c3e50; color: #ecf0f1; padding: 10px; font-family: monospace;")
        self.status_log.setAlignment(Qt.AlignmentFlag.AlignTop)
        grid.addWidget(self.status_log, 3, 0, 1, 2)
        grid.setRowStretch(3, 1)

    def update_telemetry(self, t, alt):
        """Called by ROS2Worker whenever a new odometry packet arrives."""
        self.time_data.append(t)
        self.alt_data.append(alt)
        
        # Keep only the last 300 data points (scrolling window)
        if len(self.time_data) > 300:
            self.time_data.pop(0)
            self.alt_data.pop(0)
            
        self.alt_curve.setData(self.time_data, self.alt_data)

    def launch_sim(self):
        mission = self.mission_selector.currentText()
        self.update_log(f"Initializing Sequence for: {mission}")
        px4_dir = os.path.expanduser("~/PX4-Autopilot")
        
        # Start XRCE Bridge
        self.proc_manager.launch("MicroXRCEAgent udp4 -p 8888")
        
        if "Phase 1" in mission:
            self.proc_manager.launch("HEADLESS=1 make px4_sitl gazebo-classic_iris_depth_camera", cwd=px4_dir)
            self.update_log("Gazebo Booting (Empty World)...")
        else:
            self.proc_manager.launch("HEADLESS=1 make px4_sitl gazebo-classic_iris_depth_payload__payload_obstacle_course", cwd=px4_dir)
            self.update_log("Gazebo Booting (Obstacle Course)...")
            self.proc_manager.launch("source install/setup.bash && ros2 launch uav_control mpc_obstacle_avoidance.launch.py", cwd=os.path.expanduser("~/uav-autonomous-telemetry/ros2_ws"))
            
        self.update_log("SIMULATION ACTIVE.")

    def kill_sim(self):
        self.update_log("ABORT COMMAND RECEIVED. Tearing down simulation...")
        self.proc_manager.kill_all()
        # Reset graph data
        self.time_data.clear()
        self.alt_data.clear()
        self.alt_curve.setData([], [])
        self.update_log("Simulation safely terminated.")

    def update_log(self, msg):
        current = self.status_log.text()
        lines = current.split('\n')[:15]
        self.status_log.setText(f"> {msg}\n" + '\n'.join(lines))

    def closeEvent(self, event):
        self.proc_manager.kill_all()
        self.ros_worker.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    gcs = GroundControlStation()
    gcs.show()
    sys.exit(app.exec())
