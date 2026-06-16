from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'my_sensor_station'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Launch files
        (os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        # Config files (rviz)
        (os.path.join('share', package_name, 'config'),
            glob(os.path.join('config', '*.rviz'))),
    ],
    install_requires=['setuptools', 'pyserial'],
    zip_safe=True,
    maintainer='mostafa',
    maintainer_email='mostafa.hesham.015@gmail.com',
    description='Sensor Monitoring Station with LiDAR and ultrasonic fusion',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'monitor_node = my_sensor_station.monitor_node:main',
            'arduino_bridge = my_sensor_station.arduino_bridge:main',
        ],
    },
)
