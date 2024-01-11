#!/usr/bin/env python3

import rclpy
from math import fmod, isclose
from robot_interface.msg import DriveCmd, Distance
from tamproxy import ROS2Sketch, Timer
from tamproxy.devices import Motor, Encoder, TimeOfFlight


class RobotNode(ROS2Sketch):
    """ROS2 Node that controls the Robot via the Teensy and tamproxy"""

    # Encoder clamp constant
    CLAMP = 10**7

    # PID constants
    KP = 0.00001

    # Pin mappings
    LMOTOR_PINS = (4,5)  # DIR, PWM
    RMOTOR_PINS = (2,3)  # DIR, PWM
    LENCODER_PINS = (19,20)
    RENCODER_PINS = (17,18)
    TOF_PIN = 33

    def __init__(self, rate=100):
        super().__init__(self, rate=rate)
        self.rate = rate

    def setup(self, tof_rate):
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
        timer_period = 1.0 / self.rate # convert rate to seconds
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
        self.tof = TimeOfFlight(self.tamp, self.tof_pin, 1)
        self.tof.enable()

        # Create publisher for the TOF sensor
        self.tof_publisher_ = self.create_publisher(Distance, 'distance', 10)

    def speed_to_dir_pwm(self, speed):
        """Converts floating point speed (-1.0 to 1.0) to dir and pwm values"""
        speed = max(min(speed, 1), -1)
        return speed > 0, int(abs(speed * 255))

    def timer_callback(self):
        """Publishes the teensy sensor data"""

        # Get current distance and publish it
        dist = Distance()
        dist.distance = float(self.tof.dist)
        self.get_logger().info('Publishing: "%s"' % dist.distance)
        self.publisher_.publish(dist)

    def drive_callback(self, msg):
        """Processes a new drive command and controls motors appropriately"""

        # DEPRECATED AS OF 1/11/24 :)

        # Get time
        dt = self.timer.millis()
        #self.timer.reset()

        # Store encoder values
        cur_lencoder = self.lencoder.val
        cur_rencoder = self.rencoder.val

        # Calculate error
        dlencoder = (cur_lencoder - self.prev_lencoder) * dt
        drencoder = (cur_rencoder - self.prev_rencoder) * dt
        error = (abs(dlencoder) - abs(drencoder)) * self.KP
        if abs(error) > 1: error = 0

        # Calculate adjusted left and right speeds
        l_speed = msg.l_speed - error
        r_speed = msg.r_speed + error
        """
        if isclose(msg.l_speed, 0.5) and isclose(msg.r_speed, 0.5):
            print("Straight")
        elif isclose(l_speed, -0.5) and isclose(msg.r_speed, -0.5):
            print("Reverse")
        elif isclose(msg.l_speed, 0.5) and isclose(msg.r_speed, -0.5):
            print("Right")
        elif isclose(msg.l_speed, -0.5) and isclose(msg.r_speed, 0.5):
            print("Left")
        else:
            print("Stop")
        print(error)
        """

        print(l_speed)

        # Write to the motors
        self.lmotor.write(*self.speed_to_dir_pwm(-msg.l_speed))
        self.rmotor.write(*self.speed_to_dir_pwm(msg.r_speed))

        # Store previous encoder values
        self.prev_lencoder = fmod(cur_lencoder, self.CLAMP)
        self.prev_rencoder = fmod(cur_rencoder, self.CLAMP)

def main():
    rclpy.init()

    rb = RobotNode(rate=100)  # Run at 100Hz (10ms loop)
    rb.run_setup()     # Run tamproxy setup and code in setup() method
    rclpy.spin(rb)

    rb.destroy()       # Shuts down tamproxy
    rb.destroy_node()  # Destroys the ROS node
    rclpy.shutdown()

if __name__ == '__main__':
    main()
