
#!/usr/bin/env python3

from robot_interface.msg import DriveCmd, Encoders, Cam
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
    # Encoder clamp constant
    CLAMP = 10**7

    # PID constants
    KP_DRIVE = 0.0000001
    KP_TURN = 0.05

    # Rate to check for keypresses and send commands
    RATE = 10   

    # Physical constants
    WHEEL_RADIUS = 1.9375 # inches
    BASE_WIDTH = 8.4375 # inches
    TURN_ANGLE = 1000

    def __init__(self):
        super().__init__('driver')

        #create drive publisher
        self.drive_command_publisher = self.create_publisher(
                DriveCmd,
                'drive_cmd',
                10)
        
        #subscribe to encoders
        self.encoder_sub = self.create_subscription(
            Encoders, 
            'encoders', 
            self.drive_callback, 
            10
        )

        # Subscribe to camera for angle data
        self.cam_angle_sub = self.create_subscription(
            Cam,
            'camera',
            self.calc_desired_angle,
            10
        )

        #store prev encoders
        self.prev_lencoder = 0
        self.prev_rencoder = 0

        #create timer
        self.timer = Timer()

        # Initialze wheel setpoints
        self.desired_angle = 0
        self.block_detected = False
    
    def calc_angular_velocity_setpoint(self, desired_velocity, desired_angle):
        """
        Calculates the desired angular velcoity for both motors given a forward speed and angle
        Returns: left_setpoint, right_setpoint
        """
        left_setpoint = (1 / self.WHEEL_RADIUS) * (desired_velocity - (self.BASE_WIDTH * desired_angle) / 2)
        right_setpoint = (1 / self.WHEEL_RADIUS) * (desired_velocity + (self.BASE_WIDTH * desired_angle) / 2)
        return left_setpoint, right_setpoint
    
    def calc_desired_angle(self, msg):
        """
        Calculates the new desired angle given camera data
        + is left, - is right
        """
        if np.isnan(msg.angle):
            self.desired_angle = self.TURN_ANGLE
            self.block_detected = False
        else:
            self.desired_angle = -(msg.angle * self.KP_TURN)
            self.block_detected = True

    def drive_callback(self, msg):
        # Get time
        dt = self.timer.millis()

        # Only run loop if at least 10 milliseconds have passed
        if dt >= 10:

            # Reset timer
            self.timer.reset()    
                
            # Store encoder values
            cur_lencoder = msg.lencoder
            cur_rencoder = msg.rencoder

            # Drive towards block if detected
            if self.block_detected:
                desired_speed = SPEED
                
                # Get angular velocity setpoints
                lsetpoint, rsetpoint = self.calc_angular_velocity_setpoint(desired_speed, self.desired_angle)

                # Calculate error
                wlencoder = (cur_lencoder - self.prev_lencoder) / dt
                wrencoder = (cur_rencoder - self.prev_rencoder) / dt
                lerror = (lsetpoint - wlencoder) * self.KP_DRIVE
                rerror = (rsetpoint - wrencoder) * self.KP_DRIVE
                #if abs(lerror) > 1: lerror = 0 # not sure about this line, trying to remove spikes w/o derivative

                # Calculate adjusted left and right speeds
                l_speed = desired_speed + lerror
                r_speed = desired_speed + rerror

            else:
                l_speed = TURN_SPEED
                r_speed = -TURN_SPEED

            # Publish drive speeds
            drive_cmd = DriveCmd()
            drive_cmd.l_speed = l_speed
            drive_cmd.r_speed = r_speed
            self.drive_command_publisher.publish(drive_cmd)

            # Store previous encoder values
            self.prev_lencoder = fmod(cur_lencoder, self.CLAMP)
            self.prev_rencoder = fmod(cur_rencoder, self.CLAMP)


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
