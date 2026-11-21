from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator
import rclpy

def main():
    rclpy.init()
    nav = BasicNavigator()
    nav.waitUntilNav2Active()
    goal_pose = PoseStamped()
    goal_pose.header.frame_id = "map"
    goal_pose.pose.position.x = 6.4
    goal_pose.pose.position.y = 0.55
    goal_pose.pose.orientation.w = 1.0
    nav.goToPose(goal_pose)
    while not nav.isTaskComplete():
        feedback = nav.getFeedback()
        nav.get_logger().info(f"Distance remaining: {feedback.distance_remaining:.2f} meters")
    result = nav.getResult()
    nav.get_logger().info(f"Navigation result: {result}")