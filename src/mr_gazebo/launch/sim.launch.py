from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch.substitutions import Command, FindExecutable

def generate_launch_description():
    world = LaunchConfiguration('world')
    world_arg = DeclareLaunchArgument('world', default_value='simple.world')

    world_path = PathJoinSubstitution([
        FindPackageShare('mr_gazebo'), 'worlds', world
    ])

    # Gazebo Classic launcher
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([FindPackageShare('gazebo_ros'), 'launch', 'gazebo.launch.py'])
        ]),
        launch_arguments={'world': world_path}.items()
    )

    # Robot description from xacro
    robot_description = Command([
        FindExecutable(name='xacro'), ' ',
        PathJoinSubstitution([FindPackageShare('mr_description'), 'urdf', 'mr_robot.urdf.xacro'])
    ])

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{'use_sim_time': True, 'robot_description': robot_description}],
        output='screen'
    )

    # Spawn into Gazebo
    spawner = Node(
        package='gazebo_ros', executable='spawn_entity.py', name='spawn_ddr',
        arguments=['-topic', 'robot_description', '-entity', 'ddr'],
        output='screen'
    )

    return LaunchDescription([world_arg, gazebo, rsp, spawner])
