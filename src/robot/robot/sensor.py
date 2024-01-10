
#!/usr/bin/env python3

from robot_interface.msg import sensorCmd

import rclpy

from tamproxy import ROS2Sketch
from tamproxy.devices import TimeOfFlight

RATE = 10

class TOFNode(ROS2Sketch):
    #pin of sensor on teensy
    tof_pin = 33

    def __init__(self):
        super().__init__('tof')

        # Add all ToFs
        self.tof = TimeOfFlight(self.tamp, self.tof_pin, 1)

        # Now enable them all
        self.tof.enable()

        self.tof_read_publisher = self.create_publisher(
                sensorCmd,
                'sensor_cmd',
                10)
        timer_period = 1.0 / RATE
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.distance = 15

    def timer_callback(self):
        print(self.tof.dist, "mm", "RAWRRAWRRAWRARAWRWRA")
        tof_read_msg = sensorCmd()
        tof_read_msg.tof1_distance = float(self.tof.dist)
        self.tof_read_publisher.publish(tof_read_msg)
        self.distance -= 1

def main():
    rclpy.init()

    tof = TOFNode(rate=100)  # Run at 100Hz (10ms loop)
    tof.run_setup()     # Run tamproxy setup and code in setup() method
    rclpy.spin(tof)

    tof.destroy()       # Shuts down tamproxy
    tof.destroy_node()  # Destroys the ROS node
    rclpy.shutdown()

if __name__ == "__main__":
    main()
