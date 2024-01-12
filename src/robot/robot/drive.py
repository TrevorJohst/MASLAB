
#!/usr/bin/env python3

from robot_interface.msg import DriveCmd, Encoders, Angle
from math import fmod
import rclpy
from rclpy.node import Node
from tamproxy import Timer

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

class DriverNode(Node):
    # Encoder clamp constant
    CLAMP = 10**7

    # PID constants
    KP_DRIVE = 0.00001
    KP_TURN = 0.002

    # Rate to check for keypresses and send commands
    RATE = 10   

    # Physical constants
    WHEEL_RADIUS = 1.9375 # inches
    BASE_WIDTH = 8.4375 # inches

    def __init__(self):
        super().__init__('driver')

        #create drive publisher
        self.drive_command_publisher = self.create_publisher(
                DriveCmd,
                'drive_cmd',
                10)
        
        #subscribe to encoders
        self.encoder_sub = self.create_subscription(Encoders, 'encoders', self.drive_callback, 10)

        # Subscribe to camera for angle data
        self.cam_angle_sub = self.create_subscription(
            Angle,
            'angle',
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
        self.desired_angle = -(msg.angle * self.KP_TURN)

    def drive_callback(self, msg):

        # Set desired speed based on if block is visible
        desired_speed = 0.5 if self.desired_angle == float('nan') else 0

        # Get time
        dt = self.timer.millis()
        self.timer.reset()     
        
        # Store encoder values
        cur_lencoder = msg.lencoder
        cur_rencoder = msg.rencoder
        
        # Get angular velocity setpoints
        lsetpoint, rsetpoint = self.calc_angular_velocity_setpoint(desired_speed, self.desired_angle)

        # Calculate error
        wlencoder = (cur_lencoder - self.prev_lencoder) * dt
        wrencoder = (cur_rencoder - self.prev_rencoder) * dt
        lerror = (lsetpoint - wlencoder) * self.KP_DRIVE
        rerror = (rsetpoint - wrencoder) * self.KP_DRIVE
        #if abs(lerror) > 1: lerror = 0 # not sure about this line, trying to remove spikes w/o derivative

        # Calculate adjusted left and right speeds
        l_speed = msg.l_speed + lerror
        r_speed = msg.r_speed + rerror
        
        # """
        # if isclose(msg.l_speed, 0.5) and isclose(msg.r_speed, 0.5):
        #     print("Straight")
        # elif isclose(l_speed, -0.5) and isclose(msg.r_speed, -0.5):
        #     print("Reverse")
        # elif isclose(msg.l_speed, 0.5) and isclose(msg.r_speed, -0.5):
        #     print("Right")
        # elif isclose(msg.l_speed, -0.5) and isclose(msg.r_speed, 0.5):
        #     print("Left")
        # else:
        #     print("Stop")
        # print(error)
        # """

        # print(l_speed)

        # Write to the motors
        self.lmotor.write(*self.speed_to_dir_pwm(-l_speed))
        self.rmotor.write(*self.speed_to_dir_pwm(r_speed))

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
