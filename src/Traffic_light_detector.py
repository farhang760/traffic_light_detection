#!/usr/bin/env python

import rospy
from std_msgs.msg import String, Bool, Float32
from geometry_msgs.msg import Vector3
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import darknet_library
import cv2

class TrafficLightNode:
    def __init__(self):
        rospy.init_node("traffic_light_detector", anonymous=True)

        # Initializers
        self.bridge = CvBridge()
        self.video_location = rospy.get_param("/video_address")
        self.yolo_config = rospy.get_param("/config_address")
        self.yolo_weight = rospy.get_param("/weight_address")
        self.yolo_data = rospy.get_param("/data_address")
  
   

        
        # Class variables 
        self.darknet_config = darknet_library.load_net(self.yolo_config, self.yolo_weight, 0)
        self.darknet_data = darknet_library.load_meta(self.yolo_data)

        
        
        
   
     

        # Publishers
        self.publish_detected_light = rospy.Publisher("traffic_light_detected",Bool,queue_size=10)
        self.publish_traffic_size = rospy.Publisher("traffic_light_size", Vector3, queue_size=10)
        self.publish_zone_height = rospy.Publisher("zone_height",Float32, queue_size=10)

        # Subscribers
        #self.image_sub = rospy.Subscriber("/cam/image_raw", Image, self.__CameraCallback)

    def reading_video(self):
       
        vector3_size = Vector3()


        try:
            
            video_source = cv2.VideoCapture(self.video_location)
        except CvBridgeError as e:
            rospy.loginfo(e)

        
        while(video_source.isOpened()):

            ret, cv_image = video_source.read()
            if ret == False:
                break
            resized_image = cv2.resize(cv_image,(800,600))
            detected_obj = darknet_detector.detect(self.darknet_config, self.darknet_data, resized_image)

            if len(detected_obj) and 'traffic light' in detected_obj[0]:
                x, y, w, h = detected_obj[0][2][0], detected_obj[0][2][1], detected_obj[0][2][2], detected_obj[0][2][3]
                vector3_size.x = w
                vector3_size.y = h
                vector3_size.z = 0
                self.publish_detected_light.publish(True)
                self.publish_traffic_size.publish(vector3_size)
                zone_height = vector3_size.y/ 3
                self.publish_zone_height.publish(zone_height)


            cv2.imshow("IMAGE", resized_image)
            cv2.waitKey(1)



        
def main():
    TrafficLightNode().reading_video()
    node = TrafficLightNode()
    rospy.sleep(0.5)
    rospy.spin()

if __name__ == "__main__":
    try:
        TrafficLightNode().reading_video()
    except rospy.ROSInterruptException:
        pass
