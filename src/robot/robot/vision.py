#!/usr/bin/env python3

import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge, CvBridgeError
from robot_interface.msg import Cam
from sensor_msgs.msg import Image

class VisionNode(Node):
    """
    Publisher node that interfaces with webcam and publishes angle and distance data
    Publishes 0 for angle if block is centered, + if to robot's right, - if to robot's left
    """

    # Which camera to use (should be fixed but this works for now)
    CAMERA = 0

    # Publish rate
    RATE = 100

    # Min and max HSV thresholds for green
    GREEN_THRESHOLD = ([25,45,30], [85,255,255])
    RED_THRESHOLD = ([0,160,100], [10,255,255])
    BLUE_THRESHOLD = ([100,150,80], [125,255,255])

    # Camera constants
    FOCAL_LENGTH = 472.2
    BLOCK_WIDTH = 2.375

    PTS_GROUND_PLANE = [[250, -45],
                        [295, 45],
                        [355, -75],
                        [415, 45]]

    PTS_IMAGE_PLANE = [[240, 205],
                        [102, 190],
                        [252, 164],
                        [119, 150]]

    def __init__(self, color):
        super().__init__('vision_node')
  
        #subscribe to the v4l2 camera node to extract the image
        self.v4l2_image = self.create_subscription(Image, '/image_raw', self.image_callback, 10)

        # Converts between ROS images and OpenCV Images
        self.bridge = CvBridge()

        # Create publishers
        self.angle_publisher_ = self.create_publisher(Cam, 'cam', 10)
        self.process_img_publisher_ = self.create_publisher(Image, 'processed_image', 10)

        # Store our color
        self.thresh = self.RED_THRESHOLD if color == "red" else self.GREEN_THRESHOLD

        # Get homography    
        np_pts_ground = np.array(self.PTS_GROUND_PLANE)
        np_pts_ground = np_pts_ground
        np_pts_ground = np.float32(np_pts_ground[:, np.newaxis, :])

        np_pts_image = np.array(self.PTS_IMAGE_PLANE)
        np_pts_image = np_pts_image * 1.0
        np_pts_image = np.float32(np_pts_image[:, np.newaxis, :])

        self.homog, err = cv2.findHomography(np_pts_image, np_pts_ground)

    def transformUvToXy(self, hom, u, v):
        """
        u and v are pixel coordinates. hom is homogenous matrix
        The top left pixel is the origin, u axis increases to right, and v axis
        increases down.

        Returns a normal non-np 1x2 matrix of xy displacement vector from the
        camera to the point on the ground plane.
        Camera points along positive x axis and y axis increases to the left of
        the camera.

        Units are in meters.
        """
        homogeneous_point = np.array([[u], [v], [1]])
        xy = np.dot(hom, homogeneous_point)
        scaling_factor = 1.0 / xy[2, 0]
        homogeneous_xy = xy * scaling_factor
        x = homogeneous_xy[0, 0]
        y = homogeneous_xy[1, 0]
        return x, y
    
    def image_callback(self, msg):
        # Capture a frame from the webcam
        #_, frame = self.cap.read()
        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        frame = cv2.resize(frame, (320, 240)) # resize to decrease processing

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  
        
        # Set lower and upper bounds for our team's color
        lower_bound = np.array(self.thresh[0])
        upper_bound = np.array(self.thresh[1])  

        # Set lower and upper bounds for the wall markers
        lower_blue = np.array(self.BLUE_THRESHOLD[0])
        upper_blue = np.array(self.BLUE_THRESHOLD[1])
        
        # Create a mask of our frame using our color thresholds
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Find contours from our masks
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
        blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Define angle and distance assuming no detection
        angle = np.nan
        distance = np.nan
        
        # If we have contours
        if len(contours) != 0:

            # Find the biggest countour by area
            c = max(contours, key = cv2.contourArea)

            # Get a bounding rectangle around that contour
            x, y, w, h = cv2.boundingRect(c)
                    
            y_blue = None

            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

            # If we have blue contours...
            if len(blue_contours) != 0:
                # Find the biggest countour by area
                c_blue = max(blue_contours, key = cv2.contourArea)

                # Get a bounding rectangle around that contour
                _,y_blue,_,h_blue = cv2.boundingRect(c_blue)
            
            if True or y_blue is None or (y_blue + h_blue) < y:             
                # Find center of bounding rectangle
                center_x = x + w/2
                center_y = y + h
                world_x, world_y = self.transformUvToXy(self.homog, center_x, center_y)
                distance = world_x
                angle = world_y

        # Create the camera messages
        cam_msg = Cam()
        cam_msg.angle = angle
        cam_msg.distance = distance
        self.angle_publisher_.publish(cam_msg)

        proc_img = Image()
        proc_img = self.bridge.cv2_to_imgmsg(frame, "bgr8")
        self.process_img_publisher_.publish(proc_img)
          

def main():

    rclpy.init()

    vn = VisionNode("red")
    rclpy.spin(vn)

    vn.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()