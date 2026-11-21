import rclpy
from rclpy.node import Node
from chapt4_interfaces.srv import FaceDetector
import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory
import os
from cv_bridge import CvBridge
import time
from rcl_interfaces.msg import SetParametersResult

class FaceDetectNode(Node):
    def __init__(self):
        super().__init__('face_detect_node')
        self.bridge = CvBridge()
        self.default_image_path = os.path.join(get_package_share_directory('demo_python_service'), 'resource/YYJ.jpg')
        self.get_logger().info(f"Face detection service started.")
        self.declare_parameter('number_of_times_to_upsample', 1)
        self.declare_parameter('model', 'hog')
        self.number_of_times_to_upsample = self.get_parameter('number_of_times_to_upsample').value
        self.model = self.get_parameter('model').value
        self.srv_ = self.create_service(FaceDetector, 'face_detect', self.face_detect_callback)
        self.add_on_set_parameters_callback(self.parameters_callback)

    def parameters_callback(self, params):
        for param in params:
            self.get_logger().info(f"{param.name}->{param.value}")
            if param.name == 'number_of_times_to_upsample':
                self.number_of_times_to_upsample = param.value
            elif param.name == 'model':
                self.model = param.value
        return SetParametersResult(successful=True)
    

    def face_detect_callback(self, request, response):
        # 处理人脸检测逻辑
        if request.image.data:
            cv_image = self.bridge.imgmsg_to_cv2(request.image)
        else:
            cv_image = cv2.imread(self.default_image_path)
            self.get_logger().info(f"No image provided. Using default image")

        start_time = time.time()
        self.get_logger().info('Starting face detection...')

        face_locations = face_recognition.face_locations(cv_image,
                                                         number_of_times_to_upsample=self.number_of_times_to_upsample,
                                                        model=self.model)

        response.time_used = time.time() - start_time
        response.number = len(face_locations)
        for top, right, bottom, left in face_locations:
            response.top.append(top)
            response.left.append(left)
            response.bottom.append(bottom)
            response.right.append(right)

        return response

def main():
    rclpy.init()
    node = FaceDetectNode()
    rclpy.spin(node)
    rclpy.shutdown()
