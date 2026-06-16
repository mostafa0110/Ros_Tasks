from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'robot_tf_localization'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Install launch files
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')),
        # Install config files (ekf.yaml, robot_tf.rviz)
        (os.path.join('share', package_name, 'config'),
            glob('config/*')),
        # Install Python scripts
        (os.path.join('lib', package_name),
            glob('scripts/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mostafa',
    maintainer_email='mostafa.hesham.015@gmail.com',
    description='Lab 3: TF Tree and Robot Localization with EKF',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
