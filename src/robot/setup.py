from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='team-2',
    maintainer_email='maslab-2024-team-2@mit.edu',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'robot = robot.robot:main',
            'kbd_driver = robot.kbd_driver:main',
            'driver = robot.driver:main',
            'sensor = robot.sensor:main',
            'test = robot.test:main'
        ],
    },
)
