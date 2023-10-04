import rospy
from rknn_yolo.msg import yolo
from multiprocessing.connection import Listener
import time

def run_server(host, port):  
    pub = rospy.Publisher('targets', yolo, queue_size=30)
    rospy.init_node('test', anonymous=True)
    server_sock = Listener((host, port))
    print("Sever running...", host, port)
    
    while True:
        try:
            # 接受一个新连接:
            conn = server_sock.accept()
            addr = server_sock.last_accepted
            print('Accept new connection', addr)
            while not rospy.is_shutdown():
                if conn.poll():
                    data = conn.recv()  # 等待接受数据
                    center_x, center_y, class_name = data
                    myMsg_msg = yolo()
                    myMsg_msg.center_x = center_x
                    myMsg_msg.center_y = center_y
                    myMsg_msg.class_name = class_name
                    pub.publish(myMsg_msg)
                    rospy.loginfo("center_x: %f, center_y: %f, class_name: %s", myMsg_msg.center_x, myMsg_msg.center_y, myMsg_msg.class_name)
                else:
                    pass
                    rospy.loginfo("Waiting for data...")
                    # rospy.sleep(0.1)
        except Exception as e:
            print('Socket Error,trying to reconnect...', e)
            time.sleep(1)
            
            
if __name__ == '__main__':
    server_host = '127.0.0.1'
    server_port = 22880
    try:
        run_server(server_host, server_port)
    except rospy.ROSInterruptException:
        pass