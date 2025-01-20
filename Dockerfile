# Use ROS 2 Humble base image
FROM ros:humble-ros-base

ARG OVERLAY_WS=/opt/ros/overlay_ws


# Install dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install pyzmq

# Build zmq2ROS2 from source
WORKDIR $OVERLAY_WS/src
RUN git clone https://github.com/robokal/zmq2ROS2 -b main


WORKDIR $OVERLAY_WS
RUN . /opt/ros/$ROS_DISTRO/setup.sh && \
    apt-get update && rosdep install -y \
      --from-paths src \
      --ignore-src \
    && rm -rf /var/lib/apt/lists/*

# build overlay source
RUN . /opt/ros/$ROS_DISTRO/setup.sh && \
    colcon build --symlink-install

# source entrypoint setup
ENV OVERLAY_WS $OVERLAY_WS
RUN sed --in-place --expression \
      '$isource "$OVERLAY_WS/install/setup.bash"' \
      /ros_entrypoint.sh

ENTRYPOINT ["/ros_entrypoint.sh"]

# Set up entrypoint
CMD ["/bin/bash"]
