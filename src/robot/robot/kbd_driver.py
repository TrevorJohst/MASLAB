from robot_interface.msg import DriveCmd, Encoders

import rclpy
from rclpy.node import Node
from math import fmod
import sys
import pygame
from tamproxy import Timer

# Rate to check for keypresses and send commands
RATE = 10


# Some constants for the GUI
PADDING = 32
BOX_SIZE = 64
SCREEN_SIZE = BOX_SIZE * 3 + PADDING * 2
TURN_SPEED = 0.485
SPEED = 0.501
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
    KP_DRIVE = 0.000001
    WHEEL_RADIUS = 1.9375 # inches
    BASE_WIDTH = 8.4375 # inches
    CLAMP = 10**7

    def __init__(self):
        super().__init__('keyboard_driver')
        self.screen, self.surface = pygame_setup()
        self.drive_command_publisher = self.create_publisher(
                DriveCmd,
                'drive_cmd',
                10)
        self.encoder_sub = self.create_subscription(Encoders, 'encoders', self.timer_callback, 10)
        self.timer = Timer()
        #store prev encoders
        self.prev_lencoder = 0
        self.prev_rencoder = 0


    def calc_angular_velocity_setpoint(self, desired_left, desired_right, desired_angle):
        """
        Calculates the desired angular velcoity for both motors given a forward speed and angle
        Returns: left_setpoint, right_setpoint
        """
        left_setpoint = (1 / self.WHEEL_RADIUS) * (desired_left - (self.BASE_WIDTH * desired_angle) / 2)
        right_setpoint = (1 / self.WHEEL_RADIUS) * (desired_right + (self.BASE_WIDTH * desired_angle) / 2)
        return left_setpoint, right_setpoint
    
    def timer_callback(self, msg):                
        drive_speed = calculate_drive_speed(self.screen, self.surface)

        ### DRIVE SPEED PID
        # Get time
        dt = self.timer.millis()

        # Only run loop if at least 10 milliseconds have passed
        if dt >= 10:
            self.timer.reset()    
                
            # Store encoder values
            cur_lencoder = msg.lencoder
            cur_rencoder = msg.rencoder

            l_speed = drive_speed[0]
            r_speed = drive_speed[1]
                
            # Get angular velocity setpoints
            lsetpoint, rsetpoint = self.calc_angular_velocity_setpoint(l_speed, r_speed, 0)

            # Calculate error
            wlencoder = (cur_lencoder - self.prev_lencoder) / dt
            wrencoder = (cur_rencoder - self.prev_rencoder) / dt
            lerror = (lsetpoint - wlencoder) * self.KP_DRIVE
            rerror = (rsetpoint - wrencoder) * self.KP_DRIVE
            #if abs(lerror) > 1: lerror = 0 # not sure about this line, trying to remove spikes w/o derivative

            # Calculate adjusted left and right speeds
            l_speed = l_speed + lerror
            r_speed = r_speed + rerror

            # Publish drive speeds
            drive_cmd = DriveCmd()
            drive_cmd.l_speed = l_speed
            drive_cmd.r_speed = r_speed
            self.drive_command_publisher.publish(drive_cmd)

            # Store previous encoder values
            self.prev_lencoder = fmod(cur_lencoder, self.CLAMP)
            self.prev_rencoder = fmod(cur_rencoder, self.CLAMP)
                
        ### DRIVE SPEED PID
            
        drive_cmd_msg = DriveCmd()
        drive_cmd_msg.l_speed = float(l_speed)
        drive_cmd_msg.r_speed = float(r_speed)
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