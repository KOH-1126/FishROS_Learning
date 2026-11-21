from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator
import rclpy

def main():
    rclpy.init()
    nav = BasicNavigator()
    nav.waitUntilNav2Active()
    goal_poses = []
    pose1 = PoseStamped()
    pose1.header.frame_id = "map"
    pose1.pose.position.x = 3.7
    pose1.pose.position.y = 0.4
    pose1.pose.orientation.w = 1.0

    pose2 = PoseStamped()
    pose2.header.frame_id = "map"
    pose2.pose.position.x = 5.0
    pose2.pose.position.y = 6.3
    pose2.pose.orientation.w = 1.0

    pose3 = PoseStamped()
    pose3.header.frame_id = "map"
    pose3.pose.position.x = 6.4
    pose3.pose.position.y = 0.55
    pose3.pose.orientation.w = 1.0

    goal_poses.extend([pose1, pose2, pose3])

    nav.followWaypoints(goal_poses)
    while not nav.isTaskComplete():
        feedback = nav.getFeedback()
        nav.get_logger().info(f"current waypoint: {feedback.current_waypoint}")
    result = nav.getResult()
    nav.get_logger().info(f"Navigation result: {result}")