import launch
import launch_ros

def generate_launch_description():
    """产生launch描述"""
    # 声明一个launch参数
    action_declare_arg_background = launch.actions.DeclareLaunchArgument(
        'launch_background_g', default_value="150")
    # 把launch参数传入turtlesim_node节点

    action_node_turltlesim_node = launch_ros.actions.Node(
        package='turtlesim',
        executable='turtlesim_node',
        parameters=[{
            'background_g': launch.substitutions.LaunchConfiguration('launch_background_g',
                                                                     default="150")}],
        output='screen',
    )

    action_node_patrol_client = launch_ros.actions.Node(
        package='demo_cpp_service',
        executable='patrol_client',
        output='log',
    )

    action_node_turtle_control = launch_ros.actions.Node(
        package='demo_cpp_service',
        executable='turtle_control',
        output='both',
    )
    return launch.LaunchDescription(
        [
            action_declare_arg_background,
            action_node_turltlesim_node,
            action_node_patrol_client,
            action_node_turtle_control
        ]
    )