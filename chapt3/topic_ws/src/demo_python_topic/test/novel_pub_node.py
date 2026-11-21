import rclpy
from rclpy.node import Node

class NovelPubNode(Node):
    def __init__(self, nodeName):
        super().__init__(nodeName)
        self.get_logger().info(f'{nodeName} is launched')

def main():
    rclpy.init()
    node = NovelPubNode('novel_pub_node')
    rclpy.spin(node)
    rclpy.shutdown()