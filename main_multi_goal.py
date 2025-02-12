from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from std_msgs.msg import String

class TableSubscriber(Node):
    def __init__(self, navigator):
        super().__init__('table_subscriber')
        self.navigator = navigator
        self.goal_poses = []

        # Initialize all goal poses with default values
        self.goal_pose0 = PoseStamped()
        self.goal_pose1 = PoseStamped()
        self.goal_pose2 = PoseStamped()
        self.goal_pose3 = PoseStamped()

        # Subscribe to the user input topic
        self.create_subscription(String, '/user_input_topic', self.table_callback, 10)

        # Set initial values for goal poses
        self.set_default_goal_poses()

    def table_callback(self, msg):
        table_number = msg.data
        self.get_logger().info(f"Received table: {table_number}")
        
        # Update goal_pose2 based on the received table number
        self.update_goal_pose2(table_number)
        
        # Re-follow the updated waypoints
        self.navigator.followWaypoints(self.goal_poses)

    def set_default_goal_poses(self):
        """Set initial positions for all goal poses."""
        # goal_pose0
        self.goal_pose0.header.frame_id = 'map'
        self.goal_pose0.header.stamp = self.navigator.get_clock().now().to_msg()
        self.goal_pose0.pose.position.x = -1.0257813930511475
        self.goal_pose0.pose.position.y = -0.03064233437180519
        self.goal_pose0.pose.orientation.w = 1.0
        self.goal_pose0.pose.orientation.z = 0.0

# goal_pose1
        self.goal_pose1.header.frame_id = 'map'
        self.goal_pose1.header.stamp = self.navigator.get_clock().now().to_msg()
        self.goal_pose1.pose.position.x = -3.637561559677124
        self.goal_pose1.pose.position.y = -0.011716923676431179
        self.goal_pose1.pose.orientation.w = 1.0
        self.goal_pose1.pose.orientation.z = 0.0

        # goal_pose3
        self.goal_pose3.header.frame_id = 'map'
        self.goal_pose3.header.stamp = self.navigator.get_clock().now().to_msg()
        self.goal_pose3.pose.position.x = -1.0257813930511475
        self.goal_pose3.pose.position.y = -0.03064233437180519
        self.goal_pose3.pose.orientation.w = 1.0
        self.goal_pose3.pose.orientation.z = 0.0

        # Initialize goal_pose2 with a placeholder value (it will be updated on callback)
        self.goal_pose2.header.frame_id = 'map'
        self.goal_pose2.header.stamp = self.navigator.get_clock().now().to_msg()
        self.goal_pose2.pose.orientation.w = 1.0
        self.goal_pose2.pose.orientation.z = 0.0

        # Add all goal poses to the list
        self.goal_poses = [self.goal_pose0,self.goal_pose1, self.goal_pose2, self.goal_pose3]

    def update_goal_pose2(self, table_number):
        """Update the goal pose for table2 based on the table number."""
        # Table positions for table1, table2, table3
        table_positions = {
            'table1': (1.7131673097610474, -1.8416534662246704),
            'table2': (0.1173233762383461, -4.703824996948242),
            'table3': (1.173417329788208, 2.87390398979187),
            'table4': (0.3754916191101074, 0.3754916191101074)
        }

        # If the table number is valid, update the goal pose
        if table_number in table_positions:
            x, y = table_positions[table_number]
            self.goal_pose2.pose.position.x = x
            self.goal_pose2.pose.position.y = y
            self.goal_pose2.header.stamp = self.navigator.get_clock().now().to_msg()
        else:
            self.get_logger().warn(f"Unknown table: {table_number}")

def main():
    rclpy.init()

    navigator = BasicNavigator()
    navigator.waitUntilNav2Active()

    table_subscriber = TableSubscriber(navigator)

    # Start the navigator's main loop
    try:
        rclpy.spin(table_subscriber)
    except KeyboardInterrupt:
        pass
    finally:
        table_subscriber.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
