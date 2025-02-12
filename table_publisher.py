import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time

class UserInputPublisher(Node):
    def __init__(self):
        super().__init__('user_input_publisher')
        self.publisher_ = self.create_publisher(String, 'user_input_topic', 10)
        self.get_logger().info("User Input Publisher Node has started. Type 'table 1' to 'table 4'.")
        
        # Store the current valid input
        self.current_input = None

        # Run the input loop
        self.user_input_loop()

    def user_input_loop(self):
        while rclpy.ok():
            if self.current_input:
                # If there is a valid input, keep publishing it
                msg = String()
                msg.data = self.current_input
                self.publisher_.publish(msg)
                self.get_logger().info(f"Published: {self.current_input}")
                time.sleep(1)  # Delay for 1 second before publishing again

            # Ask for new user input when the previous input is None or changed
            user_input = input("Enter 'table 1', 'table 2', 'table 3', or 'table 4': ").strip().lower()

            # Validate the input
            if user_input in ['table1', 'table2', 'table3', 'table4']:
                self.current_input = user_input
                self.get_logger().info(f"Changed input to: {self.current_input}")
            else:
                self.get_logger().warn("Invalid input. Please enter 'table 1' to 'table 4'.")

def main(args=None):
    rclpy.init(args=args)

    user_input_publisher = UserInputPublisher()

    try:
        rclpy.spin(user_input_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        user_input_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
