cmake_minimum_required(VERSION 3.8)
project(uav_control)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(px4_msgs REQUIRED)

# The Flight Controller
add_executable(offboard_control src/offboard_control.cpp)
ament_target_dependencies(offboard_control rclcpp px4_msgs)

# The New Telemetry Logger
add_executable(telemetry_logger src/telemetry_logger.cpp)
ament_target_dependencies(telemetry_logger rclcpp px4_msgs)

install(TARGETS
  offboard_control
  telemetry_logger
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
