import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator
from tf2_ros import TransformListener, Buffer, TransformException
from tf_transformations import quaternion_from_euler
from autopatrol_interfaces.srv import SpeechText
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os


class PatrolNode(BasicNavigator):
    def __init__(self, node_name='patrol_node'):
        super().__init__(node_name)
        self.declare_parameter('initial_point', [0.0, 0.0, 0.0]) # x, y, yaw
        self.declare_parameter('target_points', [0.0, 0.0, 0.0, 1.0, 1.0, 1.57]) # three elements for each point
        self.declare_parameter('img_save_path', '')
        self.buffer_ = Buffer()
        self.listener_ = TransformListener(self.buffer_, self) 
        self.speech_client_ = self.create_client(SpeechText, 'text_speaker')
        self.cv_bridge_ = CvBridge()
        self.latest_image_ = None
        self.img_sub_ = self.create_subscription(Image, '/camera_sensor/image_raw', self.image_callback, 1)

    def image_callback(self, msg):
        self.latest_image_ = msg

    def record_image(self):
        if self.latest_image_ is not None:
            cv_image = self.cv_bridge_.imgmsg_to_cv2(self.latest_image_)
            poseSaved = self.get_current_pose()
            name = f"image_{poseSaved.pose.position.x:.2f}_{poseSaved.pose.position.y:.2f}.png"
            path = os.path.join(self.get_parameter('img_save_path').value, name) 
            cv2.imwrite(path, cv_image)

    def get_pose_by_xyyaw(self, x, y, yaw):
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.pose.position.x = x
        pose.pose.position.y = y
        quaternion = quaternion_from_euler(0, 0, yaw)
        pose.pose.orientation.x = quaternion[0]
        pose.pose.orientation.y = quaternion[1]
        pose.pose.orientation.z = quaternion[2]
        pose.pose.orientation.w = quaternion[3]
        return pose

    def init_robot_pose(self):
        self.initial_point_ = self.get_parameter('initial_point').value
        self.setInitialPose(self.get_pose_by_xyyaw(*self.initial_point_))
        self.waitUntilNav2Active()

    def get_target_poses(self):
        points = []
        self.target_points_ = self.get_parameter('target_points').value
        for index in range(0, len(self.target_points_), 3):
            x = self.target_points_[index]
            y = self.target_points_[index + 1]
            yaw = self.target_points_[index + 2]
            points.append(self.get_pose_by_xyyaw(x, y, yaw))
            self.get_logger().info(f"Target point {len(points)}: x={x}, y={y}, yaw={yaw} got.")
        return points

    def nav_to_pose(self, target_pose):
        if not self.goToPose(target_pose):
            return
        while not self.isTaskComplete():
            feedback = self.getFeedback()
            if feedback is not None:
                self.get_logger().info(
                    f"Distance remaining: {feedback.distance_remaining:.2f} m")
        result = self.getResult()
        self.get_logger().info(f"Navigation result: {result}")
        
    def get_current_pose(self):
        try:
            result = self.buffer_.lookup_transform(
                'map', 'base_footprint', rclpy.time.Time())
            self.get_logger().info(f'translation: {result.transform.translation}')
            current_pose = PoseStamped()
            current_pose.header.frame_id = 'map'
            current_pose.pose.position.x = result.transform.translation.x
            current_pose.pose.position.y = result.transform.translation.y
            current_pose.pose.position.z = result.transform.translation.z
            current_pose.pose.orientation = result.transform.rotation
            return current_pose
        except TransformException as e:
            self.get_logger().error(f'Failed to get transform: {e}')    
            return None

    def ask_speech(self, text):
        while not self.speech_client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('waiting for speech service...')
        request = SpeechText.Request()
        request.text = text
        future = self.speech_client_.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        if future.result():
        # successfully called the service
            response = future.result()
            if(response.result):
                self.get_logger().info('Speech service called successfully.')
            else:
                self.get_logger().warn('Speech service call failed.')
        else:
        # failed to call the service
            self.get_logger().warn('Failure in waiting for the speech service response.')

def main():
    rclpy.init()
    patrol_node = PatrolNode()
    patrol_node.ask_speech("Starting initialization of the patrol robot.")
    patrol_node.init_robot_pose()
    patrol_node.ask_speech("Initialization complete.")
    # rclpy.spin(patrol_node)
    while rclpy.ok():
        target_poses = patrol_node.get_target_poses()
        for target_pose in target_poses:
            patrol_node.ask_speech(f"Moving to target point {target_pose.pose.position.x}, {target_pose.pose.position.y}.")
            patrol_node.nav_to_pose(target_pose)
            patrol_node.ask_speech("Arrived.")
            patrol_node.record_image()
            patrol_node.ask_speech("Image recorded.")
        break  # Exit after one loop of navigation for demonstration purposes

    rclpy.shutdown()
