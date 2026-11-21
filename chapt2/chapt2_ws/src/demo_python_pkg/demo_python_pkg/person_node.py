import rclpy
from rclpy.node import Node

class PersonNode(Node):
    def __init__(self, node_name:str, name: str, age: int) -> None:
        print('PersonNode __init__ is called with two properties added')
        super().__init__(node_name)
        self.name = name
        self.age = age 
    def eat(self, food:str) -> None:
        """
        Simulate the person eating food.
        """
        # print(f"{self.name} is eating {food}.")
        self.get_logger().info(f"{self.name} is eating {food}.")


def main():
    rclpy.init()
    node1 = PersonNode("JQY", "JIA QINGYANG", 22)
    node1.eat("beef")
    rclpy.spin(node1)
    rclpy.shutdown()