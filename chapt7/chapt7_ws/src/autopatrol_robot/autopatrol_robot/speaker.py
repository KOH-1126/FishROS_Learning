import rclpy
from rclpy.node import Node
from autopatrol_interfaces.srv import SpeechText
import espeakng

class Speaker(Node):
    def __init__(self):
        super().__init__('speaker')
        self.speaker_srv_ = self.create_service(SpeechText, 'text_speaker', self.speech_callback)
        self.speaker_ = espeakng.Speaker()

    def speech_callback(self, request, response):
        text = request.text
        self.get_logger().info(f"Received text to speak: {text}")
        self.speaker_.say(text)
        self.speaker_.wait()  # Wait for the speech to finish
        response.result = True
        return response

def main():
    rclpy.init()
    speaker_node = Speaker()
    rclpy.spin(speaker_node)
    rclpy.shutdown()
