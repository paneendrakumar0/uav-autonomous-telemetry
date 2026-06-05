#include <rclcpp/rclcpp.hpp>
#include <px4_msgs/msg/vehicle_odometry.hpp>
#include <fstream>
#include <iostream>
#include <string>

class TelemetryLogger : public rclcpp::Node {
public:
    TelemetryLogger() : Node("telemetry_logger") {
        // Create or overwrite the CSV file
        csv_file_.open("flight_trajectory.csv");
        csv_file_ << "Timestamp,X,Y,Z\n";

        // Create a QoS profile specifically matching the PX4 BestEffort requirement
        rmw_qos_profile_t qos_profile = rmw_qos_profile_sensor_data;
        auto qos = rclcpp::QoS(rclcpp::QoSInitialization(qos_profile.history, 10), qos_profile);

        // Subscribe to the drone's odometry data using the matched QoS
        odometry_subscription_ = this->create_subscription<px4_msgs::msg::VehicleOdometry>(
            "/fmu/out/vehicle_odometry", qos,
            std::bind(&TelemetryLogger::odometry_callback, this, std::placeholders::_1));

        RCLCPP_INFO(this->get_logger(), "Telemetry Logger Started with SensorData QoS. Recording to flight_trajectory.csv...");
    }

    ~TelemetryLogger() {
        if (csv_file_.is_open()) {
            csv_file_.close();
            RCLCPP_INFO(this->get_logger(), "Log saved and closed.");
        }
    }

private:
    void odometry_callback(const px4_msgs::msg::VehicleOdometry::SharedPtr msg) {
        // PX4 uses NED coordinates. Z is down, so we multiply by -1 to make altitude positive.
        float x = msg->position[0];
        float y = msg->position[1];
        float z = -msg->position[2]; 
        uint64_t time = msg->timestamp;

        csv_file_ << time << "," << x << "," << y << "," << z << "\n";
    }

    rclcpp::Subscription<px4_msgs::msg::VehicleOdometry>::SharedPtr odometry_subscription_;
    std::ofstream csv_file_;
};

int main(int argc, char *argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<TelemetryLogger>());
    rclcpp::shutdown();
    return 0;
}
