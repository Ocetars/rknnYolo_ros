import rospy
from rknn_yolo.msg import yolo
import math


def filter_point(new_point):
    global last_point, error_count
    if last_point is None:
        last_point = new_point
        return new_point
    else:
        # 计算偏差值
        deviation = math.sqrt((new_point[0] - last_point[0]) ** 2 + (new_point[1] - last_point[1]) ** 2)
        if deviation < threshold:
            last_point = new_point
            error_count = 0
            return new_point
        else:
            error_count += 1
            if error_count >= max_error_count:
                last_point = new_point
                error_count = 0
                return new_point
            else:
                return None



# 回调函数，处理接收到的 Point 消息
def point_callback(point_msg):
    # 提取 x, y值
    X_value = point_msg.center_x
    Y_value = point_msg.center_y
    class_name = point_msg.class_name
    if class_name == 'tent':  
        new_point = (X_value, Y_value)
        output_point = filter_point(new_point)
        if output_point is not None:
            point_ros = yolo()
            point_ros.center_x = output_point[0]
            point_ros.center_y = output_point[1]
            point_ros.class_name = class_name
            rospy.loginfo(point_ros)
            pub.publish(point_ros)



if __name__ == '__main__':
    rospy.init_node('filter_node_tent')
    pub = rospy.Publisher('filter_targets', yolo, queue_size=30)
    threshold = 50  # 阈值
    last_point = None  # 上一个坐标点
    error_count = 0  # 连续的误差次数
    max_error_count = 20  # 最大的连续误差次数
    sub = rospy.Subscriber('targets', yolo, point_callback)
    rospy.spin()