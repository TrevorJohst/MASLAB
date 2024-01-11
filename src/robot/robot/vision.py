#!/usr/bin/env python3

import cv2
import numpy as np
import rclpy
from rclpy.node import Node

from robot_interface.msg import Angle

class VisionNode(Node):
    """Publisher node that interfaces with webcam and publishes angle and distance data"""

    # Which camera to use (should be fixed but this works for now)
    CAMERA = 0

    # Publish rate
    RATE = 100

    # Min and max HSV thresholds for green
    GREEN_THRESHOLD = ([25,45,30], [85,255,255])
    RED_THRESHOLD = ([0,160,140], [10,255,255])

    def __init__(self, color):
        super().__init__('vision node')

        # Create angle publisher
        self.angle_publisher_ = self.create_publisher(Angle, 'angle', 10)

        # Create timer object
        timer_period = 1.0 / self.RATE # convert to seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        
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
        
        # Create a mask of our frame using our color threshold
        mask = cv2.inRange(hsv, lower_bound, upper_bound)

        # Find contours from our mask 
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
        
        # If we have contours
        if len(contours) != 0:

            # Find the biggest countour by area
            c = max(contours, key = cv2.contourArea)

            # Get a bounding rectangle around that contour
            x, y, w, h = cv2.boundingRect(c)

            # Draw the rectangle on our frame [DEBUG ONLY]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)  
            
        # Find center of bounding rectangle
        center = x + w/2

        # Create the angle message
        angle_msg = Angle()
        angle_msg.angle = 320 - center
        self.angle_publisher_.publish(angle_msg)
        self.get_logger().info('Publishing: "%s"' % angle_msg.data) # [DEBUG ONLY]
          
        # Display that frame
        cv2.imshow('frame', cv2.resize(frame, (320, 240)))

def main():

    rclpy.init()

    vn = VisionNode()
    rclpy.spin(vn)

    vn.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()