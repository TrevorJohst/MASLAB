from robot_interface.msg import DriveCmd, Gyro

import rclpy
from rclpy.node import Node
from tamproxy import Timer

import sys
import pygame

# Some constants for the GUI
PADDING = 32
BOX_SIZE = 64
SCREEN_SIZE = BOX_SIZE * 3 + PADDING * 2
TURN_SPEED = 0.485
SPEED = 0.51

KEY_SPEEDS = {
    pygame.K_w: (SPEED, SPEED),
    pygame.K_a: (-TURN_SPEED, TURN_SPEED),
    pygame.K_s: (-SPEED, -SPEED),
    pygame.K_d: (TURN_SPEED, -TURN_SPEED)
}
BOX_OFFSETS = {
    pygame.K_w: (0, -1),
    pygame.K_a: (-1, 0),
    pygame.K_s: (0, 1),
    pygame.K_d: (1, 0)
}
BG_COLOR = (255, 255, 255)
BOX_COLOR = (0, 0, 0)


def pygame_setup():
    # Setup the GUI
    pygame.init()
    pygame.display.set_caption('KitBot Keyboard Driver')
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE), 0, 32)
    surface = pygame.Surface(screen.get_size()).convert()
    return screen, surface

def calculate_drive_speed(screen, surface):
    # Calculate new drive speeds and GUI coordinates from keypresses
    drive_speed = 0, 0
    box_pos = PADDING + BOX_SIZE, PADDING + BOX_SIZE
    pressed = pygame.key.get_pressed()
    show_dir = False
    for keycode in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
        if pressed[keycode]:
            drive_speed = (drive_speed[0] + KEY_SPEEDS[keycode][0],
                           drive_speed[1] + KEY_SPEEDS[keycode][1])
            box_pos = (box_pos[0] + BOX_OFFSETS[keycode][0] * BOX_SIZE,
                       box_pos[1] + BOX_OFFSETS[keycode][1] * BOX_SIZE)
            show_dir = True

    # Update the GUI
    surface.fill(BG_COLOR)
    if show_dir:
        r = pygame.Rect(box_pos, (BOX_SIZE, BOX_SIZE))
        pygame.draw.rect(surface, BOX_COLOR, r)
    screen.blit(surface, (0, 0))
    pygame.display.flip()
    pygame.display.update()

    # Process event queue and sleep between loops
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    return drive_speed


class KeyboardDriverNode(Node):
    # PID constants
    KP_TURN = 0.05
    KD_TURN = 0.0
    KI_TURN = 0.0

    # Physical constants
    WHEEL_RADIUS = 1.9375 # inches
    BASE_WIDTH = 8.4375 # inches

    def __init__(self):
        super().__init__('keyboard_driver')
        self.screen, self.surface = pygame_setup()
        self.drive_command_publisher = self.create_publisher(
                DriveCmd,
                'drive_cmd',
                10)
        
        # Subscribe to the IMU
        self.encoder_sub = self.create_subscription(
            Gyro, 
            'gyroscope', 
            self.drive_callback, 
            10
        )

        # Store values for PID
        self.prev_error = 0
        self.integral = 0

        # Create a timer for PID
        self.timer = Timer()

        # Initialze wheel setpoints
        self.desired_angle = 0
        self.block_detected = False

    def drive_callback(self, msg):   
        drive_speed = calculate_drive_speed(self.screen, self.surface) 

        # Get time
        dt = self.timer.millis()

        # Only run loop if at least 10 milliseconds have passed
        if dt >= 10:

            # Reset timer
            self.timer.reset()    
                
            # Store gyro value
            cur_z_rate = msg.z_rate

            l_speed = drive_speed[0]
            r_speed = drive_speed[1]

            # PID error calculation
            proportional = -cur_z_rate
            derivative = (proportional - self.prev_error) / dt
            self.integral += proportional * dt
            adjustment = proportional * self.KP_TURN + derivative * self.KD_TURN + self.integral * self.KI_TURN

            # Calculate adjusted left and right speeds
            l_speed = drive_speed[0] + adjustment
            r_speed = drive_speed[1] - adjustment

            # Store previous error
            self.prev_error = proportional

        drive_cmd_msg = DriveCmd()
        drive_cmd_msg.l_speed = l_speed
        drive_cmd_msg.r_speed = r_speed
        self.drive_command_publisher.publish(drive_cmd_msg)

def main():
    rclpy.init()
    # Create an instance of KeyboardDriverNode
    keyboard_driver_node = KeyboardDriverNode()
    # Continue to run the node until a stop command is given
    rclpy.spin(keyboard_driver_node)
    # Destroy the node!
    keyboard_driver_node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()