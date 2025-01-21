import time
import zmq

def main():
    # ZMQ context and socket setup
    context = zmq.Context()
    socket = context.socket(zmq.PUB)

    # Define the ZMQ address to bind to
    zmq_address = "tcp://*:5555"
    socket.bind(zmq_address)

    print(f"ZMQ publisher is running and bound to {zmq_address}")

    # Mock message data
    counter = 0
    try:
        while True:
            # Create a simple message
            message = f"Mock message {counter}"
            counter += 1

            # Publish the message
            socket.send_string(message)
            print(f"Published: {message}")

            # Wait for 1 second before publishing the next message
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Shutting down ZMQ publisher")
    finally:
        socket.close()
        context.term()


if __name__ == "__main__":
    main()