#!/usr/bin/env python3

import rclpy
from math import fmod, isclose
from robot_interface.msg import DriveCmd, Distance, Encoders, Stops
from tamproxy import ROS2Sketch, Timer
from tamproxy.devices import Motor, Encoder, TimeOfFlight, DigitalInput


class RobotNode(ROS2Sketch):
    """ROS2 Node that controls the Robot via the Teensy and tamproxy"""
    
    # Pin mappings
    LMOTOR_PINS = (4,5)  # DIR, PWM
    RMOTOR_PINS = (2,3)  # DIR, PWM
    LENCODER_PINS = (35,36)
    RENCODER_PINS = (39,40)
    TOF_PIN = 33
    TELEVATOR_PIN = 19
    BELEVATOR_PIN = 6

    # Publish rate
    RATE = 100

    def setup(self):
        """
        One-time method that sets up the robot, like in Arduino
        Code is run when run_setup() method is called
        """
        # Create a subscriber to listen for drive motor commands
        self.drive_sub = self.create_subscription(
            DriveCmd,
            'drive_cmd',
            self.drive_callback,
            10)
        self.drive_sub  # prevent unused variable warning

        # Create timer object
        timer_period = 1.0 / self.RATE # convert rate to seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        # Create the motor objects
        self.lmotor = Motor(self.tamp, *self.LMOTOR_PINS)
        self.rmotor = Motor(self.tamp, *self.RMOTOR_PINS)

        # Create the encoder objects
        self.lencoder = Encoder(self.tamp, *self.LENCODER_PINS, continuous=True)
        self.rencoder = Encoder(self.tamp, *self.RENCODER_PINS, continuous=True)
        self.prev_lencoder = 0
        self.prev_rencoder = 0

        # Create TOF sensor object
        self.tof = TimeOfFlight(self.tamp, self.TOF_PIN, 1)
        self.tof.enable()

        # Create endstop digital readers
        self.elevator_top = DigitalInput(self.tamp, self.TELEVATOR_PIN)
        self.elevator_bottom = DigitalInput(self.tamp, self.BELEVATOR_PIN)

        # Create publisher for the sensors
        self.tof_publisher_ = self.create_publisher(Distance, 'distance', 10)
        self.enc_publisher_ = self.create_publisher(Encoders, 'encoders', 10)
        self.end_publisher_ = self.create_publisher(Stops, 'end_stops', 10)

    def speed_to_dir_pwm(self, speed):
        """Converts floating point speed (-1.0 to 1.0) to dir and pwm values"""
        speed = max(min(speed, 1), -1)
        return speed > 0, int(abs(speed * 255))

    def timer_callback(self):
        """Publishes the teensy sensor data"""

        # Get current distance and publish it
        dist = Distance()
        dist.distance = float(self.tof.dist)
        self.tof_publisher_.publish(dist)

        # Get current encoder data
        enc = Encoders()
        enc.lencoder = self.lencoder.val
        enc.rencoder = self.rencoder.val
        self.enc_publisher_.publish(enc)

        # Get endstop data
        stop = Stops()
        stop.elevator_top = True if self.elevator_top.val == bytes([1]) else False
        stop.elevator_bottom = True if self.elevator_bottom.val == bytes([1]) else False
        self.end_publisher_.publish(stop)

    def drive_callback(self, msg):
        """Processes a new drive command and controls motors appropriately"""
        # Write to the motors
        #self.get_logger().info("LSpeed: " + str(msg.l_speed))
        #self.get_logger().info("RSpeed: " + str(msg.r_speed))
        self.lmotor.write(*self.speed_to_dir_pwm(-msg.l_speed))
        self.rmotor.write(*self.speed_to_dir_pwm(msg.r_speed))

def main():
    rclpy.init()

    rb = RobotNode()
    rb.run_setup()     # Run tamproxy setup and code in setup() method
    rclpy.spin(rb)

    rb.destroy()       # Shuts down tamproxy
    rb.destroy_node()  # Destroys the ROS node
    rclpy.shutdown()

if __name__ == '__main__':
    main()
