from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator
import rclpy

def main():
    rclpy.init()
    nav = BasicNavigator()
    initial_pose = PoseStamped()
    initial_pose.header.frame_id = "map"
    initial_pose.pose.position.x = 0.0
    initial_pose.pose.position.y = 0.0
    initial_pose.pose.orientation.w = 1.0
    nav.setInitialPose(initial_pose)
    nav.waitUntilNav2Active()
    rclpy.spin(nav)
    rclpy.shutdown()