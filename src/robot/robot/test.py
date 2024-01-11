#!/usr/bin/env python3

from robot_interface.msg import Distance

import rclpy

from tamproxy import ROS2Sketch
from tamproxy.devices import TimeOfFlight

class DistanceNode(ROS2Sketch):
    """ROS2 Node that publishes distance data from TOF sensor"""

    # Pin of TOF sensor on teensy
    PIN = 33

    def __init__(self, rate=100, node_name="teensy"):
        super.__init__(rate=rate)
        self.rate = rate

    def setup(self):
        """
        One-time method that sets up the robot, like in Arduino
        Code is run when run_setup() method is called
        """
        # Add TOF sensor
        self.tof = TimeOfFlight(self.tamp, self.tof_pin, 1)

        # Enable the sensor
        self.tof.enable()

        # Create publisher for sensor data
        self.publisher_ = self.create_publisher(Distance, 'distance', 10)

        # Create a timer for publishing
        timer_period = 1.0 / self.rate # convert rate to seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        """Publishes the current distance data"""

        # Get current distance and publish it
        dist = Distance()
        dist.distance = float(self.tof.dist)
        self.get_logger().info('Publishing: "%s"' % dist.distance)
        self.publisher_.publish(dist)

def main():
    rclpy.init()

    dn = DistanceNode(rate=100)  # Run at 100Hz (10ms loop)
    dn.run_setup()     # Run tamproxy setup and code in setup() method
    rclpy.spin(dn)

    dn.destroy()       # Shuts down tamproxy
    dn.destroy_node()  # Destroys the ROS node
    rclpy.shutdown()

if __name__ == '__main__':
    main()
