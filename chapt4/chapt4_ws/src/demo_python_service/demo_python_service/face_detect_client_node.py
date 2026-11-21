import rclpy
from rclpy.node import Node
from chapt4_interfaces.srv import FaceDetector
import cv2
from ament_index_python.packages import get_package_share_directory
import os
from cv_bridge import CvBridge
from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import Parameter, ParameterValue, ParameterType

class FaceDetectClientNode(Node):
    def __init__(self):
        super().__init__('face_detect_client_node')
        self.bridge = CvBridge()
        self.default_image_path = os.path.join(get_package_share_directory('demo_python_service'), 'resource/YYJ.jpg')
        self.client = self.create_client(FaceDetector, 'face_detect')
        self.get_logger().info(f"Face detection client started.")
        self.image = cv2.imread(self.default_image_path)

    def call_set_parameters_service(self, params):
        """
        调用服务，修改参数值
        """
        # 1 创建客户端
        self.update_param_client = self.create_client(SetParameters, '/face_detect_node/set_parameters')
        while self.update_param_client.wait_for_service(timeout_sec=1.0) == False:
            self.get_logger().info('Service for changing parameters not available, waiting again...')
        # 2 创建request
        request = SetParameters.Request()
        request.parameters = params
        # 3 发送请求 更新参数
        future = self.update_param_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        response = future.result()
        return response

    def update_detect_model(self, model='hog'):
        """
        根据传入的model，构造parameters，然后调用call_set_parameters_service方法，修改参数值
        """
        # 1 创建参数对象
        param = Parameter()
        param.name = 'model'
        # 2 赋值
        param_value = ParameterValue()
        param_value.string_value = model
        param_value.type = ParameterType.PARAMETER_STRING
        param.value = param_value
        # 3 调用服务，修改参数值
        response = self.call_set_parameters_service([param])
        for result in response.results:
            if result.successful:
                self.get_logger().info(f"Parameter 'model' updated to '{model}' successfully.")
            else:
                self.get_logger().error(f"Failed to update parameter 'model': {result.reason}")


        

    def send_request(self):
        while self.client.wait_for_service(timeout_sec=1.0) == False:
            self.get_logger().info('Service not available, waiting again...')
        # 构造request
        request = FaceDetector.Request()
        request.image = self.bridge.cv2_to_imgmsg(self.image)
        # 发送请求
        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        response = future.result()
        self.get_logger().info(f"Number of faces detected: {response.number}, Time used: {response.time_used:.4f} seconds")
        # self.show_response(response)


    def show_response(self, response):
        for i in range(response.number):
            top = response.top[i]
            left = response.left[i]
            bottom = response.bottom[i]
            right = response.right[i]
            cv2.rectangle(self.image, (left, top), (right, bottom), (0, 255, 0), 4)
        cv2.namedWindow('Face Detection Result', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Face Detection Result', 1000, 700)
        cv2.imshow('Face Detection Result', self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    

def main():
    rclpy.init()
    node = FaceDetectClientNode()
    node.update_detect_model('hog')  # 修改参数值为 'hog'
    node.send_request()
    node.update_detect_model('cnn')  # 修改参数值为 'cnn'
    node.send_request()
    rclpy.spin(node)
    rclpy.shutdown()