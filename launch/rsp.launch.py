import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, Command
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    # ── 1. Khai báo tham số ───────────────────────────────────────────────
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Sử dụng thời gian mô phỏng (True) hoặc thực tế (False)'
    )

    # ── 2. Xử lý tệp URDF/Xacro bằng Command (Cách chuẩn ROS 2 Jazzy) ─────
    pkg_path = get_package_share_directory('articubot_one')
    xacro_file = os.path.join(pkg_path, 'description', 'robot.urdf.xacro')
    
    # Sử dụng Command để chạy lệnh xacro tại runtime, cho phép truyền tham số linh hoạt sau này
    robot_description_config = ParameterValue(
        Command(['xacro ', xacro_file]), 
        value_type=str
    )
    
    # ── 3. Cấu hình Node Robot State Publisher ────────────────────────────
    params = {
        'robot_description': robot_description_config, 
        'use_sim_time': use_sim_time
    }
    
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    return LaunchDescription([
        use_sim_time_arg,
        node_robot_state_publisher
    ])