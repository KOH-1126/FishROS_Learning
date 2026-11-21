import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory
# 获取功能包share的绝对路径

import os

def main():
    YYJ_PATH = \
    os.path.join(get_package_share_directory('demo_python_service') 
        ,'resource/YYJ.jpg')
    print(f"YYJ_PATH: {YYJ_PATH}")

    # 加载图片
    image = cv2.imread(YYJ_PATH)
    # 检测人脸
    face_locations = face_recognition.face_locations(image)
    # 绘制人脸框
    for top, right, bottom, left in face_locations:
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 4)
    #结果显示
    cv2.namedWindow('Face Detection', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Face Detection', 1000, 700)
    cv2.imshow('Face Detection', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

