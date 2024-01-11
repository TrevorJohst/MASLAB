
#!/usr/bin/env python3

from robot_interface.msg import DriveCmd, Encoders
from math import fmod
import rclpy
from rclpy.node import Node

import sys

TURN_SPEED = 0.485
SPEED = 0.51

# Some constants for the GUI
SPEEDS = {
    "forward": (SPEED, SPEED),
    "left": (-TURN_SPEED, TURN_SPEED),
    "right": (-SPEED, -SPEED),
    "backward": (TURN_SPEED, -TURN_SPEED)
}

def calculate_drive_speed(distance):
    # Calculate new drive speeds and GUI coordinates from keypresses
    drive_speed = 0, 0
    if (distance > 0):
            drive_speed = (drive_speed[0] + SPEEDS["front"][0],
                           drive_speed[1] + SPEEDS["front"][1])

    return drive_speed


class DriverNode(Node):
    # Encoder clamp constant
    CLAMP = 10**7

    # PID constants
    KP = 0.00001

    # Rate to check for keypresses and send commands
    RATE = 10   

    def __init__(self):
        super().__init__('driver')

        #create drive publisher
        self.drive_command_publisher = self.create_publisher(
                DriveCmd,
                'drive_cmd',
                10)
        
        #subscribe to encoders
        self.encoder_sub = self.create_subscription(Encoders, 'encoders', self.drive_callback, 10)

        #store prev encoders
        self.prev_lencoder = 0
        self.prev_rencoder = 0

    def drive_callback(self, msg):
        #calculate speed based on distance
        drive_speed = calculate_drive_speed(self.distance)
        #store speed in variables
        l_speed = drive_speed[0]
        r_speed = drive_speed[1]

        #get dt with timer
        dt = self.timer.millis()
        self.timer.reset()

        cur_lencoder = msg.lencoder
        cur_rencoder = msg.rencoder

        #math math math
        dlencoder = (cur_lencoder - self.prev_lencoder) * dt
        drencoder = (cur_rencoder - self.prev_rencoder) * dt
        error = (abs(dlencoder) - abs(drencoder)) * self.KP
        if abs(error) > 1: error = 0

        #calculate adjusted speeds
        l_speed = l_speed - error
        r_speed = r_speed + error

        #save previous encoder values
        self.prev_lencoder = fmod(cur_lencoder, self.CLAMP)
        self.prev_rencoder = fmod(cur_rencoder, self.CLAMP)

        #publish speeds to tell motors in robot.py
        drive_cmd_msg = DriveCmd()
        drive_cmd_msg.l_speed = float(l_speed)
        drive_cmd_msg.r_speed = float(r_speed)
        self.drive_command_publisher.publish(drive_cmd_msg) 

        self.distance -= 1       

def main():
    rclpy.init()
    # Create an instance of KeyboardDriverNode
    driver_node = DriverNode()
    # Continue to run the node until a stop command is given
    rclpy.spin(driver_node)
    # Destroy the node!
    driver_node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
