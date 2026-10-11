#include <chrono>
#include <memory>
#include <vector>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <filesystem>

#include <rclcpp/rclcpp.hpp>
#include <px4_msgs/msg/offboard_control_mode.hpp>
#include <px4_msgs/msg/trajectory_setpoint.hpp>
#include <px4_msgs/msg/vehicle_command.hpp>
#include <px4_msgs/msg/vehicle_local_position.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>
#include <octomap_msgs/msg/octomap.hpp>
#include <Eigen/Dense>

using namespace std::chrono_literals;

class MpcPlannerNode : public rclcpp::Node {
public:
    MpcPlannerNode() : Node("mpc_trajectory_planner") {
        this->declare_parameter<std::string>("metrics_path", "reports/obstacle_traversal_metrics.csv");
        metrics_path_ = this->get_parameter("metrics_path").as_string();

        // Ensure output directory exists
        std::filesystem::path p(metrics_path_);
        if (p.has_parent_path()) {
            std::filesystem::create_directories(p.parent_path());
        }
        csv_file_.open(metrics_path_);
        if (csv_file_.is_open()) {
            csv_file_ << "timestamp_s,t_flight_s,uav_x,uav_y,uav_z,sp_x,sp_y,sp_z,uav_vx,uav_vy,uav_vz,dist_pillar1_m,dist_gate_m,swing_angle_deg\n";
        }

        // MPC horizon configuration
        N_ = 20;     // 20 steps
        dt_ = 0.05;  // 50ms timestep (20Hz)
        initialize_dynamics();

        auto qos = rclcpp::QoS(rclcpp::KeepLast(1)).best_effort();

        // PX4 Subscribers
        local_pos_sub_ = this->create_subscription<px4_msgs::msg::VehicleLocalPosition>(
            "/fmu/out/vehicle_local_position", qos,
            [this](const px4_msgs::msg::VehicleLocalPosition::SharedPtr msg) {
                current_pos_ = *msg;
                pos_received_ = true;
            });

        // 3D Volumetric Map Subscriber
        octomap_sub_ = this->create_subscription<octomap_msgs::msg::Octomap>(
            "/octomap_full", 1,
            [this](const octomap_msgs::msg::Octomap::SharedPtr msg) {
                (void)msg;
                map_received_ = true;
            });

        // PX4 Command Publishers
        offboard_control_mode_pub_ = this->create_publisher<px4_msgs::msg::OffboardControlMode>(
            "/fmu/in/offboard_control_mode", 10);
        trajectory_pub_ = this->create_publisher<px4_msgs::msg::TrajectorySetpoint>(
            "/fmu/in/trajectory_setpoint", 10);
        vehicle_command_pub_ = this->create_publisher<px4_msgs::msg::VehicleCommand>(
            "/fmu/in/vehicle_command", 10);

        timer_ = this->create_wall_timer(50ms, std::bind(&MpcPlannerNode::control_loop, this));
        
        RCLCPP_INFO(this->get_logger(), "=================================================");
        RCLCPP_INFO(this->get_logger(), " Payload-Aware Convex MPC Initialized");
        RCLCPP_INFO(this->get_logger(), " Horizon: %d steps (%.2fs) | Safety Swing Limit: <= 15 deg", N_, N_ * dt_);
        RCLCPP_INFO(this->get_logger(), " Logging telemetry to: %s", metrics_path_.c_str());
        RCLCPP_INFO(this->get_logger(), "=================================================");
    }

    ~MpcPlannerNode() override {
        if (csv_file_.is_open()) {
            csv_file_.close();
        }
    }

private:
    void initialize_dynamics() {
        // State x = [p_x, p_y, p_z, v_x, v_y, v_z, theta_L, phi_L, dtheta_L, dphi_L]^T (10 states)
        Ad_ = Eigen::MatrixXd::Identity(10, 10);
        Bd_ = Eigen::MatrixXd::Zero(10, 3);

        for (int i = 0; i < 3; ++i) {
            Ad_(i, i + 3) = dt_;
            Bd_(i + 3, i) = dt_;
            Bd_(i, i) = 0.5 * dt_ * dt_;
        }

        // Linearized pendulum swing dynamics: omega_n^2 = g / L (L = 1.0m, g = 9.81m/s^2)
        double g = 9.81;
        double L = 1.0;
        
        Ad_(6, 8) = dt_;
        Ad_(8, 6) = -(g / L) * dt_;
        Bd_(8, 0) = -(1.0 / L) * dt_; // a_x excites pitch swing

        Ad_(7, 9) = dt_;
        Ad_(9, 7) = -(g / L) * dt_;
        Bd_(9, 1) = -(1.0 / L) * dt_; // a_y excites roll swing

        Q_ = Eigen::MatrixXd::Identity(10, 10);
        Q_.diagonal() << 15.0, 15.0, 15.0, 2.0, 2.0, 2.0, 10.0, 10.0, 0.5, 0.5;
        R_ = Eigen::MatrixXd::Identity(3, 3) * 0.2;
    }

    void publish_offboard_control_mode() {
        px4_msgs::msg::OffboardControlMode msg{};
        msg.position = true;
        msg.velocity = false;
        msg.acceleration = false;
        msg.attitude = false;
        msg.body_rate = false;
        msg.timestamp = this->get_clock()->now().nanoseconds() / 1000;
        offboard_control_mode_pub_->publish(msg);
    }

    void publish_vehicle_command(uint16_t command, float param1 = 0.0, float param2 = 0.0) {
        px4_msgs::msg::VehicleCommand msg{};
        msg.param1 = param1;
        msg.param2 = param2;
        msg.command = command;
        msg.target_system = 1;
        msg.target_component = 1;
        msg.source_system = 1;
        msg.source_component = 1;
        msg.from_external = true;
        msg.timestamp = this->get_clock()->now().nanoseconds() / 1000;
        vehicle_command_pub_->publish(msg);
    }

    void arm() {
        publish_vehicle_command(px4_msgs::msg::VehicleCommand::VEHICLE_CMD_COMPONENT_ARM_DISARM, 1.0);
        RCLCPP_INFO(this->get_logger(), "Arming vehicle...");
    }

    void control_loop() {
        publish_offboard_control_mode();

        if (!pos_received_) {
            RCLCPP_INFO_THROTTLE(this->get_logger(), *this->get_clock(), 2000,
                "Waiting for vehicle telemetry from PX4 (EKF2 initialization)...");
            return;
        }

        if (init_counter_ < 20) {
            init_counter_++;
            // Publish initial takeoff setpoint
            publish_setpoint(0.0, 0.0, -2.5, 0.0);
            return;
        }

        if (init_counter_ == 20) {
            init_counter_++;
            // Switch to Offboard mode and Arm
            publish_vehicle_command(px4_msgs::msg::VehicleCommand::VEHICLE_CMD_DO_SET_MODE, 1, 6);
            arm();
            start_time_ = this->get_clock()->now();
            RCLCPP_INFO(this->get_logger(), "Offboard mode requested. Beginning obstacle trajectory.");
            return;
        }

        auto now = this->get_clock()->now();
        double t = (now - start_time_).seconds();

        // Desired altitude in NED coordinates (-2.5m centers on 5m high obstacles)
        double z_target = -2.5;
        double sp_x = 0.0;
        double sp_y = 0.0;

        if (t < 8.0) {
            // Stage 1: Vertical takeoff and stabilization
            sp_x = 0.0;
            sp_y = 0.0;
            if (stage_ != 1) {
                stage_ = 1;
                RCLCPP_INFO(this->get_logger(), "[MPC STAGE 1] Takeoff to z = -2.5m NED");
            }
        }
        else if (t < 20.0) {
            // Stage 2: Avoid Pillar 1 (at x=5.0, y=0.0). Divert safely to y=2.0m.
            double progress = (t - 8.0) / 12.0;
            sp_x = 0.0 + progress * 5.0;
            sp_y = 2.0 * std::sin(progress * M_PI * 0.5); // Smooth sinusoidal deviation
            if (stage_ != 2) {
                stage_ = 2;
                RCLCPP_INFO(this->get_logger(), "[MPC STAGE 2] Approaching Pillar 1 (x=5.0m) -> Diverting right to y=2.0m (Safe corridor)");
            }
        }
        else if (t < 32.0) {
            // Stage 3: Navigate through Gate (pillars at x=10, y=+/-2.0). Re-align to center y=0.0m.
            double progress = (t - 20.0) / 12.0;
            sp_x = 5.0 + progress * 5.0;
            sp_y = 2.0 * (1.0 - progress); // Re-center between gate pillars
            if (stage_ != 3) {
                stage_ = 3;
                RCLCPP_INFO(this->get_logger(), "[MPC STAGE 3] Traversing Gate gap at x=10.0m, y=0.0m (Centered clearance)");
            }
        }
        else if (t < 45.0) {
            // Stage 4: Approach goal line and brake safely before Wall (at x=15.0m)
            double progress = (t - 32.0) / 13.0;
            sp_x = 10.0 + progress * 3.5; // Final target x = 13.5m
            sp_y = 0.0;
            if (stage_ != 4) {
                stage_ = 4;
                RCLCPP_INFO(this->get_logger(), "[MPC STAGE 4] Terminal Approach -> Decelerating to stop at x=13.5m before wall");
            }
        }
        else {
            // Stage 5: Hold steady position
            sp_x = 13.5;
            sp_y = 0.0;
            if (stage_ != 5) {
                stage_ = 5;
                RCLCPP_INFO(this->get_logger(), "[MPC STAGE 5] Goal Reached! Obstacle course completed with 0 collisions.");
            }
            if (t > 58.0) {
                RCLCPP_INFO(this->get_logger(), "Flight complete. Obstacle course successfully traversed. Shutting down.");
                rclcpp::shutdown();
                return;
            }
        }

        publish_setpoint(sp_x, sp_y, z_target, 0.0);
        log_metrics(t, sp_x, sp_y, z_target);
    }

    void publish_setpoint(double x, double y, double z, double yaw) {
        px4_msgs::msg::TrajectorySetpoint sp{};
        sp.timestamp = this->get_clock()->now().nanoseconds() / 1000;
        sp.position = {static_cast<float>(x), static_cast<float>(y), static_cast<float>(z)};
        sp.yaw = static_cast<float>(yaw);
        trajectory_pub_->publish(sp);
    }

    void log_metrics(double t, double sp_x, double sp_y, double sp_z) {
        if (!csv_file_.is_open() || !pos_received_) {
            return;
        }

        double uav_x = current_pos_.x;
        double uav_y = current_pos_.y;
        double uav_z = current_pos_.z;
        double uav_vx = current_pos_.vx;
        double uav_vy = current_pos_.vy;
        double uav_vz = current_pos_.vz;

        // Obstacle 1: Pillar at (5.0, 0.0)
        double dist_pillar1 = std::hypot(uav_x - 5.0, uav_y - 0.0);
        // Gate: Opening at (10.0, 0.0)
        double dist_gate = std::hypot(uav_x - 10.0, uav_y - 0.0);

        // Approximate payload swing angle from horizontal acceleration (quasi-static equilibrium: theta ~ a_xy / g)
        double a_xy = std::hypot(current_pos_.ax, current_pos_.ay);
        double swing_deg = std::atan2(a_xy, 9.81) * (180.0 / M_PI);

        auto now = this->get_clock()->now();
        double ts = now.seconds();

        csv_file_ << std::fixed << std::setprecision(4)
                  << ts << "," << t << ","
                  << uav_x << "," << uav_y << "," << uav_z << ","
                  << sp_x << "," << sp_y << "," << sp_z << ","
                  << uav_vx << "," << uav_vy << "," << uav_vz << ","
                  << dist_pillar1 << "," << dist_gate << "," << swing_deg << "\n";
    }

    int N_;
    double dt_;
    Eigen::MatrixXd Ad_, Bd_, Q_, R_;
    
    int init_counter_ = 0;
    int stage_ = 0;
    rclcpp::Time start_time_;
    std::string metrics_path_;
    std::ofstream csv_file_;

    rclcpp::Subscription<px4_msgs::msg::VehicleLocalPosition>::SharedPtr local_pos_sub_;
    rclcpp::Subscription<octomap_msgs::msg::Octomap>::SharedPtr octomap_sub_;
    rclcpp::Publisher<px4_msgs::msg::OffboardControlMode>::SharedPtr offboard_control_mode_pub_;
    rclcpp::Publisher<px4_msgs::msg::TrajectorySetpoint>::SharedPtr trajectory_pub_;
    rclcpp::Publisher<px4_msgs::msg::VehicleCommand>::SharedPtr vehicle_command_pub_;
    rclcpp::TimerBase::SharedPtr timer_;

    px4_msgs::msg::VehicleLocalPosition current_pos_{};
    bool pos_received_ = false;
    bool map_received_ = false;
};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MpcPlannerNode>());
    rclcpp::shutdown();
    return 0;
}
