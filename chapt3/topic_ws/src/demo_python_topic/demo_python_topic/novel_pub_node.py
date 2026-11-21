import rclpy
from rclpy.node import Node
import requests
from example_interfaces.msg import String
from queue import Queue


class NovelPubNode(Node):
    def __init__(self, nodeName):
        super().__init__(nodeName)
        self.get_logger().info(f'{nodeName} is launched')
        self.novel_queue = Queue()
        self.novel_publisher = self.create_publisher(String, 'novel', 20)
        self.create_timer(5, self.timer_callback)

    def timer_callback(self):
        if self.novel_queue.qsize() > 0:
            line = self.novel_queue.get()
            msg = String()
            msg.data = line
            self.novel_publisher.publish(msg)
            self.get_logger().info(f'Published: {msg}')

    def download(self, url):
        response = requests.get(url)
        response.encoding = 'utf-8'
        txt = response.text
        self.get_logger().info(f'{url} is downloaded. {len(txt)}')
        for line in txt.splitlines():
            self.novel_queue.put(line)


def main():
    rclpy.init()
    node = NovelPubNode('novel_pub_node')
    node.download(r'http://localhost:8000/PoemofFall.txt')
    rclpy.spin(node)
    rclpy.shutdown()