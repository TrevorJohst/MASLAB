
#!/usr/bin/env python3

from robot_interface.msg import DriveCmd, Encoders
from math import fmod
import rclpy
from rclpy.node import Node
from tamproxy import Timer

import sys

TURN_SPEED = 0.485
SPEED = 0.51

# Speed constants
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
    KP = 0.00001

    # Rate to check for keypresses and send commands
    RATE = 10   

    def __init__(self):
        super().__init__('driver')

        # Create drive publisher
        self.drive_command_publisher = self.create_publisher(
                DriveCmd,
                'drive_cmd',
                10)
        
        # Subscribe to encoders
        self.encoder_sub = self.create_subscription(Encoders, 'encoders', self.drive_callback, 10)

        # Store prev encoders
        self.prev_lencoder = 0
        self.prev_rencoder = 0

        # Create a timer
        self.timer = Timer()

    def drive_callback(self, msg):
        
        # Drive forward [DEBUG]
        drive_speed = SPEEDS["forward"]

        # Store speed in variables
        l_speed = drive_speed[0]
        r_speed = drive_speed[1]

        # Get change in time
        dt = self.timer.millis()
        self.timer.reset()

        # Store current encoder values
        cur_lencoder = msg.lencoder
        cur_rencoder = msg.rencoder

        # Calculate motor speeds and error
        dlencoder = (cur_lencoder - self.prev_lencoder) * dt
        drencoder = (cur_rencoder - self.prev_rencoder) * dt
        error = (abs(dlencoder) - abs(drencoder)) * self.KP
        if abs(error) > 1: error = 0

        # Adjust speeds based on error
        l_speed -= error
        r_speed += error

        # Save previous encoder values clamped to not overflow
        self.prev_lencoder = fmod(cur_lencoder, self.CLAMP)
        self.prev_rencoder = fmod(cur_rencoder, self.CLAMP)

        # Publish drive speeds
        drive_cmd_msg = DriveCmd()
        drive_cmd_msg.l_speed = float(l_speed)
        drive_cmd_msg.r_speed = float(r_speed)
        self.drive_command_publisher.publish(drive_cmd_msg) 

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
