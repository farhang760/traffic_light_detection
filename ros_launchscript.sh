#!/bin/bash
set -e


# Set the default command to execute
# when creating a new container
service nginx start &

source /opt/ros/$ROS_DISTRO/setup.bash
source /root/catkin_ws/devel/setup.bash --extend


# Start the simulation framework and put it in background
roslaunch traffic_light_detection detection.launch

exec "$@"
