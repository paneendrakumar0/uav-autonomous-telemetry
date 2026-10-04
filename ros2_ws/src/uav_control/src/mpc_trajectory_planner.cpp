#include <chrono>
#include <memory>
#include <vector>

#include <rclcpp/rclcpp.hpp>
#include <px4_msgs/msg/vehicle_odometry.hpp>
#include <px4_msgs/msg/trajectory_setpoint.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>
#include <octomap_msgs/msg/octomap.hpp>

using namespace std::chrono_literals;

class MpcPlannerNode : public rclcpp::Node {
public:
    MpcPlannerNode() : Node("mpc_trajectory_planner") {
        
        // UAV State Subscription
        uav_odom_sub_ = this->create_subscription<px4_msgs::msg::VehicleOdometry>(
            "/fmu/out/vehicle_odometry", rclcpp::SensorDataQoS(),
            [this](const px4_msgs::msg::VehicleOdometry::SharedPtr msg) {
                current_uav_odom_ = *msg;
                uav_odom_received_ = true;
            });

        // Payload State Subscription
        payload_pose_sub_ = this->create_subscription<geometry_msgs::msg::PoseStamped>(
            "/gazebo/payload_pose", 10,
            [this](const geometry_msgs::msg::PoseStamped::SharedPtr msg) {
                current_payload_pose_ = *msg;
                payload_pose_received_ = true;
            });

        // Occupancy Map Subscription (for SDF generation)
        octomap_sub_ = this->create_subscription<octomap_msgs::msg::Octomap>(
            "/octomap_full", 1,
            [this](const octomap_msgs::msg::Octomap::SharedPtr msg) {
                current_octomap_ = *msg;
                map_received_ = true;
            });

        // Trajectory Setpoint Publisher (to send optimized path to offboard node)
        trajectory_pub_ = this->create_publisher<px4_msgs::msg::TrajectorySetpoint>(
            "/fmu/in/trajectory_setpoint", 10);

        // Control Loop running at 20 Hz
        timer_ = this->create_wall_timer(50ms, std::bind(&MpcPlannerNode::control_loop, this));
        
        RCLCPP_INFO(this->get_logger(), "MPC Trajectory Planner Node Initialized.");
        RCLCPP_INFO(this->get_logger(), "Waiting for UAV Odometry, Payload Pose, and Octomap...");
    }

private:
    void control_loop() {
        if (!uav_odom_received_ || !payload_pose_received_ || !map_received_) {
            // Cannot optimize without full state feedback and map
            return;
        }

        // TODO: (Chunk 5) Formulate constraints and cost function.
        // 1. Convert Octomap to Local SDF.
        // 2. Set payload swing constraints.
        // 3. Set vehicle dynamic limits (v_max, a_max).
        // 4. Pass matrices to OSQP / Acados solver.
        
        solve_mpc();
    }

    void solve_mpc() {
        // Placeholder for Convex Optimization solver wrapper.
        // Once solved, we extract the first optimal setpoint and publish it.
        
        px4_msgs::msg::TrajectorySetpoint setpoint{};
        setpoint.timestamp = this->get_clock()->now().nanoseconds() / 1000;
        
        // Publishing dummy hover setpoint during scaffolding phase
        setpoint.position = {0.0, 0.0, -5.0};
        setpoint.yaw = 0.0;
        
        trajectory_pub_->publish(setpoint);
    }

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
