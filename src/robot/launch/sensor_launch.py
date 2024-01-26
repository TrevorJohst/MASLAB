from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='robot',
            executable='vision',
            output='screen'
        ),
        Node (
            package="v4l2_camera",
            executable="v4l2_camera_node",
            parameters=[{"camera_info_url" : "file:///home/team-2/robot_ws/src/robot/brio100.yaml"}],
            output="screen"
        )
    ])
