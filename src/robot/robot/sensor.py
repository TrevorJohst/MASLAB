
#!/usr/bin/env python3

from robot_interface.msg import SensorCmd

import rclpy

from tamproxy import ROS2Sketch
from tamproxy.devices import TimeOfFlight

RATE = 10

class TOFNode(ROS2Sketch):
    #pin of sensor on teensy
    tof_pin = 33

    def setup(self):

        # Add all ToFs
        self.tof = TimeOfFlight(self.tamp, self.tof_pin, 1)

        # Now enable them all
        self.tof.enable()

        self.tof_read_publisher = self.create_publisher(
                SensorCmd,
                'sensor_cmd',
                10)
        timer_period = 1.0 / RATE
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        tof_read_msg = SensorCmd()
        tof_read_msg.tof1_distance = float(self.tof.dist)
        self.tof_read_publisher.publish(tof_read_msg)

def main():
    rclpy.init()

    tof = TOFNode()  # Run at 100Hz (10ms loop)
    tof.run_setup()     # Run tamproxy setup and code in setup() method
    rclpy.spin(tof)

    tof.destroy()       # Shuts down tamproxy
    tof.destroy_node()  # Destroys the ROS node
    rclpy.shutdown()

if __name__ == "__main__":
    main()
