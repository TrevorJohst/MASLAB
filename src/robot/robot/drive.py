#!/usr/bin/env python3

from robot_interface.msg import DriveCmd, Cam, Gyro
from math import fmod
import numpy as np
import rclpy
from rclpy.node import Node
from tamproxy import Timer

import sys

TURN_SPEED = 0.445
SPEED = 0.501

# Some constants for the GUI
SPEEDS = {
    "forward": (SPEED, SPEED),
    "left": (-TURN_SPEED, TURN_SPEED),
    "right": (-SPEED, -SPEED),
    "backward": (TURN_SPEED, -TURN_SPEED)
}

class DriverNode(Node):

    # PID constants
    KP_TURN = 0.05
    KD_TURN = 0.0
    KI_TURN = 0.0

    # Physical constants
    WHEEL_RADIUS = 1.9375 # inches
    BASE_WIDTH = 8.4375 # inches

    def __init__(self):
        super().__init__('driver')

        # Create drive command publisher
        self.drive_command_publisher = self.create_publisher(
                DriveCmd,
                'drive_cmd',
                10)
        
        # Subscribe to the IMU
        self.encoder_sub = self.create_subscription(
            Gyro, 
            'gyroscope', 
            self.drive_callback, 
            10
        )

        # Subscribe to camera for angle data and distance
        self.cam_angle_sub = self.create_subscription(
            Cam,
            'cam',
            self.calc_desired_angle,
            10
        )

        # Store values for PID
        self.prev_error = 0
        self.integral = 0

        # Create a timer for PID
        self.timer = Timer()

        # Initialze wheel setpoints
        self.desired_angle = 0
        self.block_detected = False
    
    def calc_desired_angle(self, msg):
        """
        Calculates the new desired angle in degrees given camera data then is scaled by KP_TURN
        + is left, - is right
        """
        if np.isnan(msg.angle):
            self.desired_angle = np.nan
            self.block_detected = False
        else:
            self.desired_angle = np.rad2deg(np.arctan(-msg.angle / msg.distance))
            self.block_detected = True

    def drive_callback(self, msg):
        # Get time
        dt = self.timer.millis()

        # Only run loop if at least 10 milliseconds have passed
        if dt >= 10:

            # Reset timer
            self.timer.reset()    
                
            # Store gyro value
            cur_z_rate = msg.z_rate

            # Drive towards block if detected
            if self.block_detected:
                desired_speed = SPEED
                
                # Calculate desired rotation rate
                z_rate_setpoint = self.desired_angle / dt

                # PID error calculation
                proportional = z_rate_setpoint - cur_z_rate
                derivative = (proportional - self.prev_error) / dt
                self.integral += proportional * dt
                adjustment = proportional * self.KP_TURN + derivative * self.KD_TURN + self.integral * self.KI_TURN

                # Calculate adjusted left and right speeds
                l_speed = desired_speed + adjustment
                r_speed = desired_speed - adjustment

                # Store previous error
                self.prev_error = proportional

            else:
                l_speed = TURN_SPEED
                r_speed = -TURN_SPEED

            # Publish drive speeds
            drive_cmd = DriveCmd()
            drive_cmd.l_speed = l_speed
            drive_cmd.r_speed = r_speed
            self.drive_command_publisher.publish(drive_cmd)

def main():
    rclpy.init()
    # Create an instance of DriverNode
    driver_node = DriverNode()

    # Continue to run the node until a stop command is given
    rclpy.spin(driver_node)

    # Destroy the node!
    driver_node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
