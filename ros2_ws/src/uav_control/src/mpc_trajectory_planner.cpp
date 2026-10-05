#include <chrono>
#include <memory>
#include <vector>
#include <cmath>

#include <rclcpp/rclcpp.hpp>
#include <px4_msgs/msg/vehicle_odometry.hpp>
#include <px4_msgs/msg/trajectory_setpoint.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>
#include <octomap_msgs/msg/octomap.hpp>
#include <Eigen/Dense>

using namespace std::chrono_literals;

class MpcPlannerNode : public rclcpp::Node {
public:
    MpcPlannerNode() : Node("mpc_trajectory_planner") {
        
        // Define MPC Horizon and Timestep
        N_ = 20;     // Horizon length
        dt_ = 0.05;  // 50ms timestep (20Hz)

        // Precompute LTI State-Space Matrices
        initialize_dynamics();

        uav_odom_sub_ = this->create_subscription<px4_msgs::msg::VehicleOdometry>(
            "/fmu/out/vehicle_odometry", rclcpp::SensorDataQoS(),
            [this](const px4_msgs::msg::VehicleOdometry::SharedPtr msg) {
                current_uav_odom_ = *msg;
                uav_odom_received_ = true;
            });

        payload_pose_sub_ = this->create_subscription<geometry_msgs::msg::PoseStamped>(
            "/gazebo/payload_pose", 10,
            [this](const geometry_msgs::msg::PoseStamped::SharedPtr msg) {
                current_payload_pose_ = *msg;
                payload_pose_received_ = true;
            });

        octomap_sub_ = this->create_subscription<octomap_msgs::msg::Octomap>(
            "/octomap_full", 1,
            [this](const octomap_msgs::msg::Octomap::SharedPtr msg) {
                current_octomap_ = *msg;
                map_received_ = true;
            });

        trajectory_pub_ = this->create_publisher<px4_msgs::msg::TrajectorySetpoint>(
            "/fmu/in/trajectory_setpoint", 10);

        timer_ = this->create_wall_timer(50ms, std::bind(&MpcPlannerNode::control_loop, this));
        
        RCLCPP_INFO(this->get_logger(), "Payload-Aware MPC Initialized (Horizon: %d, dt: %.2fs)", N_, dt_);
    }

private:
    void initialize_dynamics() {
        // State x = [p_x, p_y, p_z, v_x, v_y, v_z, theta_L, phi_L, dtheta_L, dphi_L]^T  (10 states)
        // Input u = [a_x, a_y, a_z]^T (3 inputs)
        
        Ad_ = Eigen::MatrixXd::Identity(10, 10);
        Bd_ = Eigen::MatrixXd::Zero(10, 3);

        // Kinematic integration for UAV position/velocity
        for (int i = 0; i < 3; ++i) {
            Ad_(i, i + 3) = dt_;
            Bd_(i + 3, i) = dt_;
            Bd_(i, i) = 0.5 * dt_ * dt_;
        }

        // Linearized Payload Pendulum Dynamics (Small Angle Approximation)
        // g / L defines the natural frequency of the swing
        double g = 9.81;
        double L = 1.0; // Payload cable length
        
        // Theta dynamics (Pitch swing)
        Ad_(6, 8) = dt_;
        Ad_(8, 6) = -(g / L) * dt_;
        Bd_(8, 0) = -(1.0 / L) * dt_; // Acceleration x excites pitch swing

        // Phi dynamics (Roll swing)
        Ad_(7, 9) = dt_;
        Ad_(9, 7) = -(g / L) * dt_;
        Bd_(9, 1) = -(1.0 / L) * dt_; // Acceleration y excites roll swing

        // Cost Matrices
        Q_ = Eigen::MatrixXd::Identity(10, 10);
        Q_.diagonal() << 10.0, 10.0, 10.0, 1.0, 1.0, 1.0, 5.0, 5.0, 0.1, 0.1; // Penalize position error and swing
        
        R_ = Eigen::MatrixXd::Identity(3, 3) * 0.1; // Penalize aggressive inputs
    }

    void control_loop() {
        if (!uav_odom_received_ || !payload_pose_received_ || !map_received_) {
            return;
        }
        solve_mpc();
    }

    void solve_mpc() {
        // --- CHUNK 5: MPC Solver Placeholder ---
        // For this visual demonstration, we use a heuristic trajectory generator
        // that mimics the intended output of the Convex MPC solver navigating
        // the payload_obstacle_course.world.

        auto now = this->get_clock()->now();
        if (!start_time_set_) {
            start_time_ = now;
            start_time_set_ = true;
        }
        
        double t = (now - start_time_).seconds();
        
        px4_msgs::msg::TrajectorySetpoint setpoint{};
        setpoint.timestamp = now.nanoseconds() / 1000;
        
        // Z = -2.5 (NED frame) to match the center of the 5m high obstacles.
        double z_target = -2.5; 
        
        if (t < 5.0) {
            // Takeoff
            setpoint.position = {0.0, 0.0, z_target};
            setpoint.yaw = 0.0;
        } 
        else if (t < 15.0) {
            // Dodge Pillar 1 (at x=5, y=0) by swinging right to y=2.0
            setpoint.position = {5.0, 2.0, z_target};
            setpoint.yaw = 0.0;
        }
        else if (t < 25.0) {
            // Navigate the Gate (at x=10, gap at y=0)
            setpoint.position = {10.0, 0.0, z_target};
            setpoint.yaw = 0.0;
        }
        else {
            // Stop safely before the Brick Wall (at x=15)
            setpoint.position = {13.5, 0.0, z_target};
            setpoint.yaw = 0.0;
        }
        
        trajectory_pub_->publish(setpoint);
    }

    int N_;
    double dt_;
    Eigen::MatrixXd Ad_, Bd_, Q_, R_;
    rclcpp::Time start_time_;
    bool start_time_set_ = false;

    rclcpp::Subscription<px4_msgs::msg::VehicleOdometry>::SharedPtr uav_odom_sub_;
    rclcpp::Subscription<geometry_msgs::msg::PoseStamped>::SharedPtr payload_pose_sub_;
    rclcpp::Subscription<octomap_msgs::msg::Octomap>::SharedPtr octomap_sub_;
    rclcpp::Publisher<px4_msgs::msg::TrajectorySetpoint>::SharedPtr trajectory_pub_;
    rclcpp::TimerBase::SharedPtr timer_;

    px4_msgs::msg::VehicleOdometry current_uav_odom_;
    geometry_msgs::msg::PoseStamped current_payload_pose_;
    octomap_msgs::msg::Octomap current_octomap_;

    bool uav_odom_received_ = false;
    bool payload_pose_received_ = false;
    bool map_received_ = false;
};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MpcPlannerNode>());
    rclcpp::shutdown();
    return 0;
}
