import zmq
import zmq.asyncio
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import asyncio
from rclpy.executors import MultiThreadedExecutor
import threading

# Define constant variables for network communication
DEFAULT_ZMQ_ADDRESS = "tcp://localhost:5555"
ZMQ_SUBSCRIBE_FILTER = ""
ROS_TOPIC_NAME = 'zmq_to_ros'

class ZMQToROSAsyncNode(Node):

    def __init__(self):
        super().__init__('zmq_to_ros_async_node')
        # create ROS publisher
        self.publisher = self.create_publisher(String, ROS_TOPIC_NAME, 10)
        self.get_logger().info("ZMQ to ROS node is up and running")

        # declate zmq communication parameters
        self.zmq_address = self.declare_parameter('zmq_address', DEFAULT_ZMQ_ADDRESS).get_parameter_value().string_value
        self.zmq_topic = self.declare_parameter('zmq_topic', ZMQ_SUBSCRIBE_FILTER).get_parameter_value().string_value

        # ZMQ socket setup
        context = zmq.asyncio.Context()

        self.subscriber = context.socket(zmq.SUB)
        self.subscriber.connect(self.zmq_address)
        self.subscriber.setsockopt_string(zmq.SUBSCRIBE, ZMQ_SUBSCRIBE_FILTER)

        self.get_logger().info(f"Listening to ZMQ topic '{self.zmq_topic}' on '{self.zmq_address}' and publishing to ROS topic '{ROS_TOPIC_NAME}'.")

        # starting loop for receiving zmq message in async
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.zmq_listener())

    async def zmq_listener(self):
        while rclpy.ok():
            try:
                # receive zmq message
                message = await self.subscriber.recv_string()
                topic, data = message.split(' ', 1)

                # create ros message
                ros_message = String()
                ros_message.data = data

                # publish ros message
                self.publisher.publish(ros_message)
                self.get_logger().info(f"Published: {data}")
            except Exception as e:
                self.get_logger().error(f"Error receiving ZMQ message: {e}")
                break

def main(args=None):
    rclpy.init(args=args)

    # create node
    node = ZMQToROSAsyncNode()

    try:
        # running zmq asyncio loop
        node.get_logger().info("Starting asyncio loop")
        node.loop.run_forever()
    except KeyboardInterrupt:
        node.get_logger().info('Node stopped by user.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()