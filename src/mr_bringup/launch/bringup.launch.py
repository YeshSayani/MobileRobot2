from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node


def generate_launch_description():
    # Param file for Nav2 nodes
    params_file = LaunchConfiguration('params_file')

    params_arg = DeclareLaunchArgument(
        'params_file',
        default_value=PathJoinSubstitution([
            FindPackageShare('mr_bringup'),
            'config',
            'nav2.yaml'
        ])
    )

    # Include Nav2 bringup. We set slam:=True and also pass a tiny placeholder map
    # to satisfy bringup's required 'map' argument on some Humble variants.
    nav2_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('nav2_bringup'),
                'launch',
                'bringup_launch.py'
            ])
        ]),
        launch_arguments={
            'use_sim_time': 'True',
            'slam': 'True',
            'map': PathJoinSubstitution([
                FindPackageShare('mr_bringup'),
                'maps',
                'placeholder.yaml'
            ]),
            'params_file': params_file,
            'autostart': 'True',
            # If your nav2_bringup supports it, you can also pass:
            # 'slam_params_file': PathJoinSubstitution([
            #     FindPackageShare('mr_bringup'), 'config', 'slam_toolbox.yaml'
            # ])
        }.items()
    )

    # RViz (optional)
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=[
            '-d',
            PathJoinSubstitution([
                FindPackageShare('mr_bringup'),
                'rviz',
                'nav2_view.rviz'
            ])
        ],
        output='screen'
    )

    return LaunchDescription([
        params_arg,
        nav2_bringup,
        rviz,
    ])
