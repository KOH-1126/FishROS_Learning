import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # 获取功能包的路径
    urdf_package_path = get_package_share_directory('fishbot_description')
    default_xacro_file_path = os.path.join(urdf_package_path, 'URDF', 'fishbot/fishbot.urdf.xacro')
    default_gazebo_world_file_path = os.path.join(urdf_package_path, 'world',
                                                  'custom_room.world')
    # 声明参数
    action_declare_arg_model_path = launch.actions.DeclareLaunchArgument(
        name='model',
        default_value=default_xacro_file_path,
        description='Absolute path to robot xacro file'
    )
    # 执行xacro命令，生成urdf文件
    command_robot_description = \
    launch.substitutions.Command(['xacro ', launch.substitutions.LaunchConfiguration('model')])

    # 运行发布者
    robot_description_param = \
    launch_ros.parameter_descriptions.ParameterValue(
        command_robot_description,
        value_type=str)

    action_robot_state_publisher = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description_param}],
    )

    action_spawn_entity = launch_ros.actions.Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', '/robot_description', '-entity', 'fishbot'])

    # 运行gazebo仿真
    action_launch_gazebo = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py'),
        ),
        launch_arguments=[('world', default_gazebo_world_file_path), ('verbose', 'true')]
    )

    action_load_joint_state_controller = launch.actions.ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', 'fishbot_joint_state_broadcaster', '--set-state', 'active'],
        output='screen'
    )

    action_load_effort_controller = launch.actions.ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', 'fishbot_effort_controller', '--set-state', 'active'],
        output='screen'
    )

    action_load_diff_drive_controller = launch.actions.ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', 'fishbot_diff_drive_controller', '--set-state', 'active'],
        output='screen'
    )

    return launch.LaunchDescription([
        action_declare_arg_model_path,
        action_robot_state_publisher,
        action_launch_gazebo,
        action_spawn_entity,
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=action_spawn_entity,
                on_exit=[action_load_joint_state_controller],
            )
        ),
        # launch.actions.RegisterEventHandler(
        #     event_handler=launch.event_handlers.OnProcessExit(
        #         target_action=action_load_joint_state_controller,
        #         on_exit=[action_load_effort_controller],
        #     )
        # )
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=action_load_joint_state_controller,
                on_exit=[action_load_diff_drive_controller],
            )
        )
    ]) 