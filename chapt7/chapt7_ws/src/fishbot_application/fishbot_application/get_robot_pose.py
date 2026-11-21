import rclpy
from rclpy.node import Node
from tf2_ros import TransformListener, Buffer # 坐标监听器
from tf_transformations import euler_from_quaternion # 四元数转欧拉角

class TFListener(Node):
    def __init__(self):
        super().__init__('tf_listener')
        self.buffer_ = Buffer()
        self.listener_ = TransformListener(self.buffer_, self) 
        self.timer_ = self.create_timer(1, self.get_transform) 

    def get_transform(self):
        """
        实时查询坐标关系
        """
        try:
            result = self.buffer_.lookup_transform('map', 'base_footprint', 
                                                   rclpy.time.Time(seconds=0.0), rclpy.time.Duration(seconds=1.0))
            transform = result.transform
            self.get_logger().info(f'translation: {transform.translation}')
            self.get_logger().info(f'rotation: {transform.rotation}')
            rotation_euler = euler_from_quaternion(
                [transform.rotation.x,
                transform.rotation.y,
                transform.rotation.z,
                transform.rotation.w]
            )
            self.get_logger().info(f'rotation (euler): {rotation_euler}')
        except Exception as e:
            self.get_logger().error(f'Failed to get transform: {e}')

def main():
    rclpy.init() # 初始化rclpy
    node = TFListener() # 创建节点对象
    rclpy.spin(node) # 循环等待回调函数
    rclpy.shutdown() # 关闭rclpy