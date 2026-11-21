import rclpy
from rclpy.node import Node

def main():
    rclpy.init()  # 初始化工作，分配资源
    node = Node('python_node')  # 创建一个节点对象
    node.get_logger().warn('Python node has been started.')  # 打印日志信息
    rclpy.spin(node)
    rclpy.shutdown()
