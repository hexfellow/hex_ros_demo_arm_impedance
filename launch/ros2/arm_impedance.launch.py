#!/usr/bin/env python3
# -*- coding:utf-8 -*-
################################################################
# Copyright 2026 Dong Zhaorui. All rights reserved.
# Author: Dong Zhaorui 847235539@qq.com
# Date  : 2026-06-30
################################################################

from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    comp_pkg_path = FindPackageShare('hex_ros_arm_comp')
    urdf_pkg_path = FindPackageShare('hex_ros_urdf_archer_y6')

    # arm_comp node
    comp_param_path = PathJoinSubstitution(
        [comp_pkg_path, "config", "ros2", "params.yaml"])
    urdf_file_path = PathJoinSubstitution(
        [urdf_pkg_path, "urdf", "gr100_comp.urdf"])

    arm_comp_node = Node(
        package='hex_ros_arm_comp',
        executable='arm_comp',
        name='arm_comp',
        output="screen",
        emulate_tty=True,
        parameters=[
            comp_param_path,
            {
                "model_urdf": ParameterValue(urdf_file_path, value_type=str),
                "use_sim_time": True,
            },
        ],
        remappings=[
            ('manip_state', 'manip_state'),
            ('manip_ctrl', 'manip_ctrl'),
            ('teleop_keyboard_state', 'teleop_keyboard_state'),
        ],
    )

    return LaunchDescription([
        arm_comp_node,
    ])
