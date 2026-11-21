import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from rclpy import qos
from rclpy.duration import Duration
from rclpy.qos import QoSProfile



class OdomPublisherSubscriber(Node):

    def __init__(self):
        super().__init__('odom_publisher_subscriber')
        # 创建发布者 reliability为best_effort
        self.odom_publisher = self.create_publisher(Odometry, 'odom', qos.qos_profile_sensor_data)
        # 创建订阅者（默认QoS配置）队列深度设置为 5 reliability为reliable
        self.odom_subscriber = self.create_subscription(
            Odometry, 'odom', self.odom_callback, qos.qos_profile_sensor_data)
        # 创建一个1秒的定时器，并指定回调函数
        self.timer = self.create_timer(1.0, self.timer_callback)

    def odom_callback(self, msg):
        self.get_logger().info('收到里程计消息')

    def timer_callback(self):
        odom_msg = Odometry()  # 创建一个Odometry消息
        self.odom_publisher.publish(odom_msg)  # 发布消息


def main(args=None):
    rclpy.init(args=args)
    odom_node = OdomPublisherSubscriber()
    rclpy.spin(odom_node)
    rclpy.shutdown()