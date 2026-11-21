import rclpy
from rclpy.node import Node
from tf2_ros import StaticTransformBroadcaster # 静态坐标发布器
from geometry_msgs.msg import TransformStamped # 消息接口
from tf_transformations import quaternion_from_euler # 欧拉角转四元数
import math # 角度转弧度函数

class StaticTFBroadcaster(Node):
    def __init__(self):
        super().__init__('static_tf_broadcaster')
        self.static_broadcaster_ = StaticTransformBroadcaster(self) # 创建静态坐标发布器对象
        self.publish_static_tf() # 发布静态坐标

    def publish_static_tf(self):
        """
        发布静态tf, from base_link to camera_link
        """
        transform= TransformStamped() # 创建TransformStamped对象
        transform.header.frame_id = 'base_link' # 父坐标系
        transform.child_frame_id = 'camera_link' # 子坐标系
        transform.header.stamp = self.get_clock().now().to_msg() # 时间戳

        transform.transform.translation.x = 0.5 # 平移
        transform.transform.translation.y = 0.3
        transform.transform.translation.z = 0.6

        # 欧拉角转四元数
        quat = quaternion_from_euler(math.radians(180), 0, 0)
        transform.transform.rotation.x = quat[0] # 旋转
        transform.transform.rotation.y = quat[1]
        transform.transform.rotation.z = quat[2]
        transform.transform.rotation.w = quat[3]

        # 发布静态坐标
        self.static_broadcaster_.sendTransform(transform)
        self.get_logger().info('Static transform from base_link to camera_link published.')

def main():
    rclpy.init() # 初始化rclpy
    node = StaticTFBroadcaster() # 创建节点对象
    rclpy.spin(node) # 循环等待回调函数
    rclpy.shutdown() # 关闭rclpy