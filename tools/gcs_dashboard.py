#!/usr/bin/env python3
import sys
import os
import signal
import subprocess
import time
import math
import csv
from datetime import datetime

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QComboBox, QGroupBox, QGridLayout
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QFont, QImage, QPixmap

import pyqtgraph as pg

import rclpy
from rclpy.node import Node
from px4_msgs.msg import VehicleOdometry
from sensor_msgs.msg import Image

# ==============================================================================
# Phase 1: Subprocess Manager (The Execution Engine)
# ==============================================================================
class SubprocessManager:
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
# Phase 1, 3, 4: ROS 2 Worker Thread
# ==============================================================================
class ROS2Worker(QThread):
    log_signal = pyqtSignal(str)
    telemetry_signal = pyqtSignal(float, float) # time, altitude
    video_signal = pyqtSignal(QImage) # FPV video frame

    def __init__(self):
        super().__init__()
        self.node = None
        self.start_time = time.time()

    def run(self):
        rclpy.init()
        self.node = rclpy.create_node('gcs_telemetry_listener')
        
        self.odom_sub = self.node.create_subscription(
            VehicleOdometry, '/fmu/out/vehicle_odometry', self.odom_callback, 10
        )
        
        self.image_sub = self.node.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10
        )
        
        self.log_signal.emit("ROS 2 Telemetry Node Initialized. Subscribed to Odometry & Video.")
        rclpy.spin(self.node)
        
    def odom_callback(self, msg):
        t = time.time() - self.start_time
        alt = -msg.position[2]
        if math.isfinite(alt):
            self.telemetry_signal.emit(t, alt)

    def image_callback(self, msg):
        try:
            q_img = QImage(
                msg.data, 
                msg.width, 
                msg.height, 
                msg.step, 
                QImage.Format.Format_RGB888
            ).copy()
            self.video_signal.emit(q_img)
        except Exception as e:
            pass

    def stop(self):
        if self.node:
            self.node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
        self.quit()
        self.wait()

# ==============================================================================
# Phase 1-5: Main Ground Control Station Window
# ==============================================================================
class GroundControlStation(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UAV Autonomous Telemetry - Ground Control Station")
        self.resize(1100, 800)

        self.proc_manager = SubprocessManager()
        self.time_data = []
        self.alt_data = []
        
        self.init_ui()

        self.ros_worker = ROS2Worker()
        self.ros_worker.log_signal.connect(self.update_log)
        self.ros_worker.telemetry_signal.connect(self.update_telemetry)
        self.ros_worker.video_signal.connect(self.update_video)
        self.ros_worker.start()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        grid = QGridLayout(main_widget)
        
        header = QLabel("GROUND CONTROL STATION - UAV SLUNG PAYLOAD")
        header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("color: #ecf0f1; background-color: #34495e; padding: 10px;")
        grid.addWidget(header, 0, 0, 1, 2)

        # Panel 1a: Mission Command Deck
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
        grid.addWidget(cmd_group, 1, 0, 1, 1)

        # Panel 1b: Phase 5 Chaos & Analytics
        chaos_group = QGroupBox("Chaos Injection & Analytics")
        chaos_group.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid #7f8c8d; margin-top: 10px; }")
        chaos_layout = QVBoxLayout()
        
        self.btn_wind = QPushButton("🌪️ INJECT 5m/s CROSSWIND")
        self.btn_wind.setStyleSheet("background-color: #e67e22; color: white; font-weight: bold; padding: 15px;")
        self.btn_wind.clicked.connect(self.inject_wind)
        
        self.btn_report = QPushButton("📊 EXPORT FLIGHT REPORT (CSV)")
        self.btn_report.setStyleSheet("background-color: #8e44ad; color: white; font-weight: bold; padding: 15px;")
        self.btn_report.clicked.connect(self.export_report)
        
        chaos_layout.addWidget(self.btn_wind)
        chaos_layout.addWidget(self.btn_report)
        chaos_group.setLayout(chaos_layout)
        grid.addWidget(chaos_group, 1, 1, 1, 1)

        # Panel 2: Telemetry
        self.telemetry_group = QGroupBox("Live Telemetry Stream: Drone Altitude")
        self.telemetry_group.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid #7f8c8d; margin-top: 10px; }")
        tel_layout = QVBoxLayout()
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

        # Panel 3: Perception Suite
        self.vision_group = QGroupBox("Perception Suite (Live FPV & Mapping)")
        self.vision_group.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid #7f8c8d; margin-top: 10px; }")
        vis_layout = QVBoxLayout()
        
        self.video_label = QLabel("Waiting for Camera Feed...")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet("background-color: #000000; color: #ffffff;")
        self.video_label.setMinimumSize(320, 240)
        vis_layout.addWidget(self.video_label)
        
        self.btn_rviz = QPushButton("🗺️ Launch RViz2 (3D Pointcloud)")
        self.btn_rviz.setStyleSheet("background-color: #2980b9; color: white; font-weight: bold; padding: 10px;")
        self.btn_rviz.clicked.connect(lambda: self.proc_manager.launch("rviz2"))
        vis_layout.addWidget(self.btn_rviz)
        
        self.vision_group.setLayout(vis_layout)
        grid.addWidget(self.vision_group, 2, 1, 1, 1)

        # Status Log
        self.status_log = QLabel("System Ready. Select a mission and Launch...")
        self.status_log.setStyleSheet("background-color: #2c3e50; color: #ecf0f1; padding: 10px; font-family: monospace;")
        self.status_log.setAlignment(Qt.AlignmentFlag.AlignTop)
        grid.addWidget(self.status_log, 3, 0, 1, 2)
        grid.setRowStretch(3, 1)

    def inject_wind(self):
        """Phase 5: Simulates a wind gust in Gazebo."""
        self.update_log("⚠️ CHAOS INJECTION: Firing 5m/s Crosswind Gust...")
        cmd = "gz topic -p '/gazebo/default/wind' -m 'linear_velocity: {x: 0, y: 5.0, z: 0}'"
        self.proc_manager.launch(cmd)

    def export_report(self):
        """Phase 5: Exports the live telemetry buffer to a CSV file."""
        if not self.time_data:
            self.update_log("❌ ERROR: No flight data to export yet.")
            return
            
        reports_dir = "/workspaces/uav-autonomous-telemetry/reports"
        os.makedirs(reports_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(reports_dir, f"gcs_flight_log_{timestamp}.csv")
        
        try:
            with open(filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Time (s)', 'Altitude (m)'])
                for t, alt in zip(self.time_data, self.alt_data):
                    writer.writerow([t, alt])
            self.update_log(f"✅ SUCCESS: Flight Report saved to {filepath}")
        except Exception as e:
            self.update_log(f"❌ ERROR: Failed to save report: {e}")

    def update_video(self, q_img):
        pixmap = QPixmap.fromImage(q_img)
        self.video_label.setPixmap(pixmap.scaled(self.video_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def update_telemetry(self, t, alt):
        self.time_data.append(t)
        self.alt_data.append(alt)
        if len(self.time_data) > 300:
            self.time_data.pop(0)
            self.alt_data.pop(0)
        self.alt_curve.setData(self.time_data, self.alt_data)

    def launch_sim(self):
        mission = self.mission_selector.currentText()
        self.update_log(f"Initializing Sequence for: {mission}")
        px4_dir = os.path.expanduser("~/PX4-Autopilot")
        
        self.proc_manager.launch("MicroXRCEAgent udp4 -p 8888")
        
        if "Phase 1" in mission:
            self.proc_manager.launch("HEADLESS=1 make px4_sitl gazebo-classic_iris_depth_camera", cwd=px4_dir)
            self.update_log("Gazebo Booting (Empty World)...")
        else:
            self.proc_manager.launch("HEADLESS=1 make px4_sitl gazebo-classic_iris_depth_payload__payload_obstacle_course", cwd=px4_dir)
            self.update_log("Gazebo Booting (Obstacle Course)...")
            self.proc_manager.launch("source install/setup.bash && ros2 launch uav_control mpc_obstacle_avoidance.launch.py", cwd="/workspaces/uav-autonomous-telemetry/ros2_ws")
            
        self.update_log("SIMULATION ACTIVE.")

    def kill_sim(self):
        self.update_log("ABORT COMMAND RECEIVED. Tearing down simulation...")
        self.proc_manager.kill_all()
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
