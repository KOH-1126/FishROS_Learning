import rclpy
from demo_python_pkg.person_node import PersonNode

class WriterNode(PersonNode):
    def __init__(self, name_node:str, name:str, age:int, book: str) -> None:
        print("WriterNode __init__ is called")
        super().__init__(name_node, name, age)
        self.book = book
        


def main():
    rclpy.init()
    node = WriterNode("YYJ", "YAN YUNJIA", 22, "YYJ is an idiot")
    node.eat("noodles")
    rclpy.spin(node)
    rclpy.shutdown()