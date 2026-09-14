#!/usr/bin/env python3
# -*- coding:utf-8 -*-
################################################################
# Copyright 2026 Dong Zhaorui. All rights reserved.
# Author: Dong Zhaorui 847235539@qq.com
# Date  : 2026-08-13
################################################################

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import GroupAction
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PathJoinSubstitution
from launch.substitutions import PythonExpression
from launch_ros.actions import PushRosNamespace
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    arm_pkg_path = FindPackageShare('hex_ros_robot_arm')
    keyboard_pkg_path = FindPackageShare('hex_ros_teleop_keyboard')
    impedance_pkg_path = FindPackageShare('hex_ros_demo_arm_impedance')

    # Left robot arguments
    left_robot_type_arg = DeclareLaunchArgument(
        name='left_robot_type',
        default_value='firefly',
        choices=['archer', 'firefly'],
        description='Left robot arm type: archer or firefly')
    left_robot_host_arg = DeclareLaunchArgument(
        name='left_robot_host',
        # default_value='192.168.1.100',
        default_value='172.18.20.80',
        description='Left robot controller IP address')
    left_robot_port_arg = DeclareLaunchArgument(
        name='left_robot_port',
        default_value='8439',
        description='Left robot controller WebSocket port')
    left_robot_grip_type_arg = DeclareLaunchArgument(
        name='left_robot_grip_type',
        default_value='empty',
        choices=['gp100', 'gp80', 'gr100', 'empty'],
        description='Left robot grip type')

    # Right robot arguments
    right_robot_type_arg = DeclareLaunchArgument(
        name='right_robot_type',
        default_value='firefly',
        choices=['archer', 'firefly'],
        description='Right robot arm type: archer or firefly')
    right_robot_host_arg = DeclareLaunchArgument(
        name='right_robot_host',
        # default_value='192.168.1.101',
        default_value='172.18.20.80',
        description='Right robot controller IP address')
    right_robot_port_arg = DeclareLaunchArgument(
        name='right_robot_port',
        default_value='9439',
        description='Right robot controller WebSocket port')
    right_robot_grip_type_arg = DeclareLaunchArgument(
        name='right_robot_grip_type',
        default_value='empty',
        choices=['gp100', 'gp80', 'gr100', 'empty'],
        description='Right robot grip type')

    left_robot_launch_file = PythonExpression(
        ['"', LaunchConfiguration('left_robot_type'), '.launch.py"'])
    right_robot_launch_file = PythonExpression(
        ['"', LaunchConfiguration('right_robot_type'), '.launch.py"'])

    left_robot_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([arm_pkg_path, left_robot_launch_file])),
        launch_arguments={
            'robot_host': LaunchConfiguration('left_robot_host'),
            'robot_port': LaunchConfiguration('left_robot_port'),
            'robot_grip_type': LaunchConfiguration('left_robot_grip_type'),
            'test': 'false',
        }.items(),
    )
    right_robot_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([arm_pkg_path, right_robot_launch_file])),
        launch_arguments={
            'robot_host': LaunchConfiguration('right_robot_host'),
            'robot_port': LaunchConfiguration('right_robot_port'),
            'robot_grip_type': LaunchConfiguration('right_robot_grip_type'),
            'test': 'false',
        }.items(),
    )

    left_impedance_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [impedance_pkg_path, 'arm_impedance.launch.py'])),
        launch_arguments={
            'use_sim_time': 'false',
            'keyboard_topic': '/teleop_keyboard_state',
        }.items(),
    )
    right_impedance_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [impedance_pkg_path, 'arm_impedance.launch.py'])),
        launch_arguments={
            'use_sim_time': 'false',
            'keyboard_topic': '/teleop_keyboard_state',
        }.items(),
    )

    keyboard_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [keyboard_pkg_path, 'teleop_keyboard.launch.py'])),
    )

    return LaunchDescription([
        left_robot_type_arg,
        left_robot_host_arg,
        left_robot_port_arg,
        left_robot_grip_type_arg,
        right_robot_type_arg,
        right_robot_host_arg,
        right_robot_port_arg,
        right_robot_grip_type_arg,
        GroupAction([
            PushRosNamespace('left'),
            left_robot_launch,
            left_impedance_launch,
        ]),
        GroupAction([
            PushRosNamespace('right'),
            right_robot_launch,
            right_impedance_launch,
        ]),
        keyboard_launch,
    ])
