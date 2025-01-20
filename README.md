# zmq2ROS2 

This package generates ROS2 messages from zmq messages

## clone the package
```mkdir ~/ros2_ws/src```

in ~/ros2_ws/src:

```git clone https://github.com/robokal/zmq2ROS2 -b main```
## build the docker
in ~/ros2_ws/src/zmq2ROS2

```docker build -t zmq_to_ros_node .```

## run the docker
```docker run -it --rm --network host zmq_to_ros_node```

inside the docker you can run the executable -> 

ros2 run zmq2ROS2 zmq_to_ros