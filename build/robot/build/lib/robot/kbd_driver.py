from robot_interface.msg import DriveCmd

import rclpy
from rclpy.node import Node

import sys
import pygame

# Rate to check for keypresses and send commands
RATE = 10

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
    def __init__(self):
        super().__init__('keyboard_driver')
        self.screen, self.surface = pygame_setup()
        self.drive_command_publisher = self.create_publisher(
                DriveCmd,
                'drive_cmd',
                10)
        timer_period = 1.0 / RATE
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):                
        drive_speed = calculate_drive_speed(self.screen, self.surface)
        drive_cmd_msg = DriveCmd()
        drive_cmd_msg.l_speed = float(drive_speed[0])
        drive_cmd_msg.r_speed = float(drive_speed[1])
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