import zmq
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

# Define constant variables for network communication
DEFAULT_ZMQ_ADDRESS = "tcp://localhost:5555"
ZMQ_SUBSCRIBE_FILTER = ""


class ZmqToRosNode(Node):
    

    def __init__(self):
        super().__init__('zmq_to_ros_node')
        self.publisher = self.create_publisher(String, 'zmq_to_ros_topic', 10)
        self.get_logger().info("ZMQ to ROS node is up and running")

        # ZMQ socket setup
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        zmq_address = self.declare_parameter("zmq_address", DEFAULT_ZMQ_ADDRESS).value
        self.socket.connect(zmq_address)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, ZMQ_SUBSCRIBE_FILTER)

        # Create a timer to poll and publish messages
        self.timer = self.create_timer(0.1, self.publish_message)

    def publish_message(self):
        try:
            # Receive ZMQ message, non-blocking
            zmq_message = self.socket.recv_string(flags=zmq.NOBLOCK)

            # create ROS message
            ros_message = String()
            ros_message.data = zmq_message
            
            # publish ROS message
            self.publisher.publish(ros_message)
            self.get_logger().info(f"Published message: {zmq_message}")
        except zmq.Again:
            pass  # No message received, non-blocking call


def main(args=None):
    rclpy.init(args=args)
    node = ZmqToRosNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down node")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()