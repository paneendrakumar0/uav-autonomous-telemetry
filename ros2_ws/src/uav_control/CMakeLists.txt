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

# Continuous Figure-8 offboard controller
add_executable(figure8_offboard src/figure8_offboard.cpp)
ament_target_dependencies(figure8_offboard rclcpp px4_msgs)

# Constant-position hover controller
add_executable(hover_offboard src/hover_offboard.cpp)
ament_target_dependencies(hover_offboard rclcpp px4_msgs)

# Geometric attitude/thrust Figure-8 prototype
add_executable(geometric_figure8_attitude src/geometric_figure8_attitude.cpp)
ament_target_dependencies(geometric_figure8_attitude rclcpp px4_msgs)

# The New Telemetry Logger
add_executable(telemetry_logger src/telemetry_logger.cpp)
ament_target_dependencies(telemetry_logger rclcpp px4_msgs)

# Figure-8 tracking metrics logger
add_executable(figure8_metrics_logger src/figure8_metrics_logger.cpp)
ament_target_dependencies(figure8_metrics_logger rclcpp px4_msgs)

install(TARGETS
  offboard_control
  figure8_offboard
  hover_offboard
  geometric_figure8_attitude
  telemetry_logger
  figure8_metrics_logger
  DESTINATION lib/${PROJECT_NAME}
)

install(PROGRAMS
  scripts/payload_swing_logger
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
