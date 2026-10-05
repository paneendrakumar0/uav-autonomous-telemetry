#!/usr/bin/env python3
import sys
import os
import signal
import subprocess
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QFont

import rclpy
from rclpy.node import Node

# ==============================================================================
# Phase 1: Subprocess Manager (The Execution Engine)
# ==============================================================================
class SubprocessManager:
    """Safely spins up and tears down bash commands and background processes."""
    def __init__(self):
        self.processes = []

    def launch(self, cmd, cwd=None):
        """Launches a process in a new session so it can be cleanly killed later."""
        print(f"[GCS] Launching: {cmd}")
        # preexec_fn=os.setsid creates a process group, allowing us to kill all children cleanly
        p = subprocess.Popen(
            cmd, shell=True, cwd=cwd,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid
        )
        self.processes.append(p)
        return p

    def kill_all(self):
        """Sends SIGTERM to all process groups managed by this instance."""
        print("[GCS] Initiating emergency teardown...")
        for p in self.processes:
            try:
                os.killpg(os.getpgid(p.pid), signal.SIGTERM)
            except ProcessLookupError:
                pass
        self.processes.clear()
        
        # Hard failsafe for zombie Gazebo/PX4 nodes
        subprocess.run("pkill -9 px4 2>/dev/null", shell=True)
        subprocess.run("pkill -9 gzserver 2>/dev/null", shell=True)
        subprocess.run("pkill -9 gzclient 2>/dev/null", shell=True)
        print("[GCS] Teardown complete. All processes killed.")

# ==============================================================================
# Phase 1: ROS 2 Worker Thread
# ==============================================================================
class ROS2Worker(QThread):
    """Runs rclpy.spin() in the background to prevent GUI freezing."""
    # Signals to communicate with the PyQt Main Thread
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.node = None

    def run(self):
        rclpy.init()
        self.node = rclpy.create_node('gcs_telemetry_listener')
        self.log_signal.emit("ROS 2 Telemetry Node Initialized.")
        
        # We will add subscriptions here in Phase 3
        
        rclpy.spin(self.node)

    def stop(self):
        if self.node:
            self.node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
        self.quit()
        self.wait()

# ==============================================================================
# Phase 1 & 2: Main Ground Control Station Window
# ==============================================================================
class GroundControlStation(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UAV Autonomous Telemetry - Ground Control Station")
        self.resize(800, 600)

        self.proc_manager = SubprocessManager()
        
        # Initialize UI Layout
        self.init_ui()

        # Start ROS 2 Worker Thread
        self.ros_worker = ROS2Worker()
        self.ros_worker.log_signal.connect(self.update_log)
        self.ros_worker.start()

from PyQt6.QtWidgets import QComboBox, QGroupBox, QGridLayout

# ... (imports handled by the file already, just redefining the class methods)
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
        cmd_group.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid #7f8c8d; margin-top: 10px; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; }")
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

        # Panel 2: Telemetry Oscilloscopes (Placeholder for Phase 3)
        self.telemetry_group = QGroupBox("Live Telemetry Stream")
        self.telemetry_group.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid #7f8c8d; margin-top: 10px; }")
        tel_layout = QVBoxLayout()
        tel_layout.addWidget(QLabel("[Phase 3: PyQtGraph Oscilloscopes will dock here]"))
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
        grid.setRowStretch(3, 1) # Allow log to expand

    def launch_sim(self):
        mission = self.mission_selector.currentText()
        self.update_log(f"Initializing Sequence for: {mission}")
        
        px4_dir = os.path.expanduser("~/PX4-Autopilot")
        
        # 1. Start XRCE Bridge
        self.proc_manager.launch("MicroXRCEAgent udp4 -p 8888")
        
        # 2. Start specific environment based on Mission Selector
        if "Phase 1" in mission:
            self.proc_manager.launch("HEADLESS=1 make px4_sitl gazebo-classic_iris_depth_camera", cwd=px4_dir)
            self.update_log("Gazebo Booting (Empty World)...")
            self.update_log("Run 'ros2 launch uav_control figure8_experiment.launch.py' manually for now.")
        else:
            self.proc_manager.launch("HEADLESS=1 make px4_sitl gazebo-classic_iris_depth_payload__payload_obstacle_course", cwd=px4_dir)
            self.update_log("Gazebo Booting (Obstacle Course)...")
            # In Phase 6 we built the master launch file for MPC
            self.proc_manager.launch("source install/setup.bash && ros2 launch uav_control mpc_obstacle_avoidance.launch.py", cwd=os.path.expanduser("~/uav-autonomous-telemetry/ros2_ws"))
            
        self.update_log("SIMULATION ACTIVE.")

    def kill_sim(self):
        self.update_log("ABORT COMMAND RECEIVED. Tearing down simulation...")
        self.proc_manager.kill_all()
        self.update_log("Simulation safely terminated.")

    def update_log(self, msg):
        current = self.status_log.text()
        # Keep log from getting infinitely long
        lines = current.split('\n')[:15]
        self.status_log.setText(f"> {msg}\n" + '\n'.join(lines))

    def closeEvent(self, event):
        """Ensures clean teardown when the X button is clicked."""
        self.proc_manager.kill_all()
        self.ros_worker.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Simple dark theme
    app.setStyle("Fusion")
    
    gcs = GroundControlStation()
    gcs.show()
    sys.exit(app.exec())
