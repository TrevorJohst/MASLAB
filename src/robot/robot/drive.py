
#!/usr/bin/env python3

from kitware_interface.msg import DriveCmd

import rclpy
from rclpy.node import Node

import sys

# Rate to check for keypresses and send commands
RATE = 10

# Some constants for the GUI
SPEEDS = {
    "forward": (0.80, 0.80),
    "left": (0.80, -0.80),
    "right": (-0.80, -0.80),
    "backward": (-0.80, 0.80)
}

def calculate_drive_speed(distance):
    # Calculate new drive speeds and GUI coordinates from keypresses
    drive_speed = 0, 0
    if (distance > 0):
            drive_speed = (drive_speed[0] + SPEEDS["front"][0],
                           drive_speed[1] + SPEEDS["front"][1])

    return drive_speed


class DriverNode(Node):
    def __init__(self):
        super().__init__('driver')

        self.drive_command_publisher = self.create_publisher(
                DriveCmd,
                'drive_cmd',
                10)
        timer_period = 1.0 / RATE
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.distance = 15

    def timer_callback(self):
        drive_speed = calculate_drive_speed(self.distance)
        drive_cmd_msg = DriveCmd()
        drive_cmd_msg.l_speed = float(drive_speed[0])
        drive_cmd_msg.r_speed = float(drive_speed[1])
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
