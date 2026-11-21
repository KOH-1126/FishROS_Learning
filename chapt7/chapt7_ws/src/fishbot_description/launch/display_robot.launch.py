import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    urdf_package_path = get_package_share_directory('fishbot_description')
    default_xacro_file_path = os.path.join(urdf_package_path, 'URDF', 'fishbot/fishbot.urdf.xacro')
    default_rviz_config_file_path = os.path.join(urdf_package_path, 
                                                 'config', 'display_robot_model.rviz')

    action_declare_arg_model_path = launch.actions.DeclareLaunchArgument(
        name='model',
        default_value=default_xacro_file_path,
        description='Absolute path to robot xacro file'
    )

    command_robot_description = \
    launch.substitutions.Command(['xacro ', launch.substitutions.LaunchConfiguration('model')])

    robot_description_param = \
    launch_ros.parameter_descriptions.ParameterValue(
        command_robot_description,
        value_type=str)

    action_robot_state_publisher = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description_param}],
    )

    action_joint_state_publisher = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher')

    action_rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', default_rviz_config_file_path],)

    return launch.LaunchDescription([
        action_declare_arg_model_path,
        action_robot_state_publisher,
        action_joint_state_publisher,
        action_rviz_node
    ])