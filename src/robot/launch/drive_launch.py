from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='robot',
            executable='robot',
            output='screen'
        ),
        Node(
            package='robot',
            executable='drive',
            output='screen'
        )
    ])

