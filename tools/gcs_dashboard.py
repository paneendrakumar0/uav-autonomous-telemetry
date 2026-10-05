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

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Header
        header = QLabel("MISSION DASHBOARD (V1.0 Scaffolding)")
        header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        # Control Buttons
        btn_layout = QHBoxLayout()
        
        self.btn_launch = QPushButton("🚀 LAUNCH SIMULATION")
        self.btn_launch.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 15px;")
        self.btn_launch.clicked.connect(self.launch_sim)
        
        self.btn_kill = QPushButton("🛑 ABORT / KILL ALL")
        self.btn_kill.setStyleSheet("background-color: #c0392b; color: white; font-weight: bold; padding: 15px;")
        self.btn_kill.clicked.connect(self.kill_sim)

        btn_layout.addWidget(self.btn_launch)
        btn_layout.addWidget(self.btn_kill)
        layout.addLayout(btn_layout)

        # Status Log
        self.status_log = QLabel("System Ready. Awaiting Command...")
        self.status_log.setStyleSheet("background-color: #2c3e50; color: #ecf0f1; padding: 10px; font-family: monospace;")
        self.status_log.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.status_log)

    def launch_sim(self):
        self.update_log("Launching MicroXRCEAgent & Gazebo Simulator...")
        
        # Paths based on standard setup
        workspace_dir = os.path.expanduser("~/uav-autonomous-telemetry")
        px4_dir = os.path.expanduser("~/PX4-Autopilot") # Assumes native or docker mount
        
        # Start the Agent
        self.proc_manager.launch("MicroXRCEAgent udp4 -p 8888")
        
        # Start Gazebo and PX4 (We use headless in Phase 1 testing to save GPU)
        self.proc_manager.launch(f"HEADLESS=1 make px4_sitl gazebo-classic_iris_depth_payload__payload_obstacle_course", cwd=px4_dir)
        
        self.update_log("Simulation Launch Initiated. Allow 10 seconds for Gazebo to boot.")

    def kill_sim(self):
        self.update_log("ABORT COMMAND RECEIVED. Tearing down simulation...")
        self.proc_manager.kill_all()
        self.update_log("Simulation safely terminated. All processes killed.")

    def update_log(self, msg):
        current = self.status_log.text()
        self.status_log.setText(f"{msg}\n{current}")

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
