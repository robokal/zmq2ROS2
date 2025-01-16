from setuptools import find_packages, setup

package_name = 'zmq2ROS2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools','pyzmq'],
    zip_safe=True,
    maintainer='lihi',
    maintainer_email='lihi@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
          'zmq_to_ros = zmq2ROS2.zmq_to_ros_node:main',
        ],
    },
)
