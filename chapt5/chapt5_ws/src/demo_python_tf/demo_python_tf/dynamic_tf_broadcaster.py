import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster # 坐标发布器
from geometry_msgs.msg import TransformStamped # 消息接口
from tf_transformations import quaternion_from_euler # 欧拉角转四元数
import math # 角度转弧度函数

class TFBroadcaster(Node):
    def __init__(self):
        super().__init__('tf_broadcaster')
        self.broadcaster_ = TransformBroadcaster(self) # 创建坐标发布器对象
        self.timer_ = self.create_timer(0.01, self.publish_tf) # 创建定时器，周期为0.01s，回调函数为publish_tf

    def publish_tf(self):
        """
        发布动态tf, from base_camera to camera_bottle
        """
        transform= TransformStamped() # 创建TransformStamped对象
        transform.header.frame_id = 'camera_link' # 父坐标系
        transform.child_frame_id = 'bottle_link' # 子坐标系
        transform.header.stamp = self.get_clock().now().to_msg() # 时间戳

        transform.transform.translation.x = 0.2 # 平移
        transform.transform.translation.y = 0.3
        transform.transform.translation.z = 0.5

        # 欧拉角转四元数
        quat = quaternion_from_euler(0, 0, 0)
        transform.transform.rotation.x = quat[0] # 旋转
        transform.transform.rotation.y = quat[1]
        transform.transform.rotation.z = quat[2] 
        transform.transform.rotation.w = quat[3]

        # 发布动态坐标
        self.broadcaster_.sendTransform(transform)
        self.get_logger().info('Dynamic transform from camera_link to bottle_link published.')

def main():
    rclpy.init() # 初始化rclpy
    node = TFBroadcaster() # 创建节点对象
    rclpy.spin(node) # 循环等待回调函数
    rclpy.shutdown() # 关闭rclpy