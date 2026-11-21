import espeakng
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from queue import Queue
import threading
import time

class NovelSubNode(Node):
    def __init__(self, nodeName):
        super().__init__(nodeName)
        self.get_logger().info(f'{nodeName} is launched')
        self.novel_queue = Queue()
        self.novel_subscriber = self.create_subscription(String, 'novel', self.novel_callback, 20)
        self.speech_thread = threading.Thread(target=self.speaking)
        self.speech_thread.start()

    def novel_callback(self, msg):
        self.novel_queue.put(msg.data)

    def speaking(self):
        speaker = espeakng.Speaker()
        speaker.voice = 'en'

        while rclpy.ok():
            if self.novel_queue.qsize() > 0:
                line = self.novel_queue.get()
                self.get_logger().info(f'Speaking: {line}')
                speaker.say(line)
                speaker.wait()
            else:
                time.sleep(1)
        

def main():
    rclpy.init()
    node = NovelSubNode('novel_sub_node')
    rclpy.spin(node)
    rclpy.shutdown()
