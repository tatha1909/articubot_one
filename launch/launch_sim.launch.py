import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    LogInfo,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

from launch_ros.actions import Node


def generate_launch_description():

    package_name = 'articubot_one' 

    pkg_share = get_package_share_directory(package_name)

    # ── 1. Khai báo các Launch Arguments ──────────────────────────────────
    world_arg = DeclareLaunchArgument(
        'world',
        default_value='empty.sdf', 
        description='obstacles.sdf'
    )

    world_path = PathJoinSubstitution([
        pkg_share, 'worlds', LaunchConfiguration('world')
    ])

    # ── 2. Robot State Publisher (Xử lý URDF/Xacro) ───────────────────────
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(pkg_share, 'launch', 'rsp.launch.py')
        ]),
        launch_arguments={'use_sim_time': 'true'}.items()
    )

    # ── 3. Gazebo Harmonic ────────────────────────────────────────────────
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch', 'gz_sim.launch.py'
            )
        ]),
        launch_arguments={
            'gz_args': ['-r -v1 ', world_path], 
            'on_exit_shutdown': 'true'
        }.items()
    )

    # ── 4. Spawn robot vào Gazebo ─────────────────────────────────────────
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        name='spawn_my_bot',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'my_bot',
            '-z', '0.1',
            '-world', 'default'
        ],
        output='screen'
    )

    # ── 5. ROS-Gazebo Bridge (Qua YAML file) ──────────────────────────────
    bridge_params = os.path.join(pkg_share, 'config', 'gz_bridge.yaml')

    ros_gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='ros_gz_bridge',
        parameters=[{
            'config_file': bridge_params,
            'use_sim_time': True,
        }],
        output='screen'
    )

    ros_gz_image_bridge = Node(
        package="ros_gz_image",
        executable="image_bridge",
        arguments=["/camera/image_raw"],
        parameters=[{'use_sim_time': True}],
        output='screen',
    )

    # ── 6. Log Info hiển thị Terminal ─────────────────────────────────────
    log = LogInfo(msg=[
        '\n========================================\n',
        '  Simulation: Gazebo Harmonic\n',
        '  ROS 2 Jazzy | Ubuntu 24.04\n',
        '========================================\n',
        '  Package : ', package_name, '\n',
        '  World   : ', LaunchConfiguration('world'), '\n',
        '  Bridge  : ', bridge_params, '\n',
        '========================================',
    ])

    return LaunchDescription([
        world_arg,
        log,
        rsp,
        gazebo,
        spawn_entity,
        ros_gz_bridge,
        ros_gz_image_bridge,
    ])