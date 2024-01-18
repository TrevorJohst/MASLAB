#!/usr/bin/env python3

import cv2
import numpy as np
import rclpy
from rclpy.node import Node

from robot_interface.msg import Cam

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

    def __init__(self, color):
        super().__init__('vision_node')

        # Create angle publisher
        self.angle_publisher_ = self.create_publisher(Cam, 'cam', 10)

        # Create timer object
        timer_period = 1.0 / self.RATE # convert to seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        # VideoCapture object we can use to get frames from webcam
        self.cap = cv2.VideoCapture(self.CAMERA)

        # Store our color
        self.thresh = self.RED_THRESHOLD if color == "red" else self.GREEN_THRESHOLD

    def timer_callback(self):

        # Capture a frame from the webcam
        _, frame = self.cap.read()
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
        
        # If we have contours
        if len(contours) != 0:

            # Find the biggest countour by area
            c = max(contours, key = cv2.contourArea)

            # Get a bounding rectangle around that contour
            x, y, w, _ = cv2.boundingRect(c)
                    
            y_blue = None

            # If we have blue contours...
            if len(blue_contours) != 0:
                # Find the biggest countour by area
                c_blue = max(blue_contours, key = cv2.contourArea)

                # Get a bounding rectangle around that contour
                _,y_blue,_,h_blue = cv2.boundingRect(c_blue)
            
            if y_blue is None or (y_blue + h_blue) < y:             
                # Find center of bounding rectangle
                center = x + w/2
                angle = center - 160
                distance = (self.BLOCK_WIDTH * self.FOCAL_LENGTH) / w
            else:
                angle = np.nan
                distance = np.nan
        else:
            angle = np.nan
            distance = np.nan

        # Create the camera message
        cam_msg = Cam()
        cam_msg.angle = angle
        cam_msg.distance = distance
        self.angle_publisher_.publish(cam_msg)
          

def main():

    rclpy.init()

    vn = VisionNode("red")
    rclpy.spin(vn)

    vn.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()