#!/usr/bin/env python3

import rclpy
from robot_interface.msg import DriveCmd, LinCmd, ColorDetect, Stops, Break
from tamproxy import ROS2Sketch, Timer
from tamproxy.devices import Motor, FeedbackMotor, DigitalInput, Color


class RobotNode(ROS2Sketch):
    """ROS2 Node that controls the Robot via the Teensy and tamproxy"""
    
    # Pin mappings
    LMOTOR_PINS = (41,15)  # DIR, PWMs
    RMOTOR_PINS = (14,13)  # DIR, PWM
    LENCODER_PINS = (31,32) # WHITE, YELLOW
    RENCODER_PINS = (35,36) # WHITE, YELLOW

    LINAC_PINS = (22,23) # DIR, PWM
    TELEVATOR_PIN = 4
    BELEVATOR_PIN = 6

    BEAM_PIN = 3

    # Publish rate
    RATE = 100

    # RGB thresholds
    RED_THRESH = 0
    GREEN_THRESH = 0

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
            10
        )
        self.drive_sub  # prevent unused variable warning

        # Create a subscriber to listen for linear actuator commands
        self.lin_sub = self.create_subscription(
            LinCmd,
            'lin_cmd',
            self.lin_callback,
            10
        )
        # Create timer object
        timer_period = 1.0 / self.RATE # convert rate to seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        # Create the motor objects
        self.lmotor = FeedbackMotor(self.tamp, *self.LMOTOR_PINS, *self.LENCODER_PINS, True)
        self.rmotor = FeedbackMotor(self.tamp, *self.RMOTOR_PINS, *self.RENCODER_PINS, True)
        self.linac = Motor(self.tamp, *self.LINAC_PINS)

        # Create endstop digital readers
        self.elevator_top = DigitalInput(self.tamp, self.TELEVATOR_PIN)
        self.elevator_bottom = DigitalInput(self.tamp, self.BELEVATOR_PIN)
	
        # Create breakbeam digital reader
        self.beamBroken = DigitalInput(self.tamp, self.BEAM_PIN)

        # Create color reader
        self.color = Color(self.tamp)

        # Create publisher for the sensors
        self.end_publisher_ = self.create_publisher(Stops, 'end_stops', 10)
        self.beam_publisher_ = self.create_publisher(Break, 'beam', 10)
        self.color_publisher_ = self.create_publisher(ColorDetect, 'color', 10)

    def timer_callback(self):
        """Publishes the teensy sensor data"""

        # Get endstop data
        stop = Stops()
        stop.elevator_top = True #if self.elevator_top.val == bytes([1]) else False
        stop.elevator_bottom = True if self.elevator_bottom.val == bytes([1]) else False
        self.end_publisher_.publish(stop)

        # Get breakbeam data
        beam = Break()
        beam.BeamBroken = True if self.beamBroken.val == bytes([1]) else False
        self.beam_publisher_.publish(beam)

        # Get updated color detection
        detect = ColorDetect()
        if self.color.r > self.RED_THRESH:
            detect.color = "Red"
        elif self.color.g > self.GREEN_THRESH:
            detect.color = "Green"
        else:
            detect.color = "None"
        self.color_publisher_.publish(detect)
	

    def speed_to_dir_pwm(self, speed):
        """Converts floating point speed (-1.0 to 1.0) to dir and pwm values"""
        speed = max(min(speed, 1), -1)
        return speed > 0, int(abs(speed * 255))

    def drive_callback(self, msg):
        """Processes a new drive command and controls motors appropriately"""
        # Write to the motors
        self.lmotor.write(msg.l_speed)
        self.rmotor.write(-msg.r_speed)

    def lin_callback(self, msg):
        # Extend or retract based on message bool
        if msg.extended:
            self.linac.write(*self.speed_to_dir_pwm(1.0))
        else:
            self.linac.write(*self.speed_to_dir_pwm(-1.0))

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
