import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # ── Khai báo các tham số linh hoạt ────────────────────────────────────
    serial_port_arg = DeclareLaunchArgument(
        'serial_port',
        default_value='/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.3:1.0-port0',
        description='Cổng kết nối vật lý của LiDAR'
    )

    frame_id_arg = DeclareLaunchArgument(
        'frame_id',
        default_value='laser_frame',
        description='Frame ID phải khớp với URDF'
    )

    baud_rate_arg = DeclareLaunchArgument(
        'baud_rate',
        default_value='460800', # Dùng lidar C1
        description='Tốc độ truyền dữ liệu của LiDAR'
    )

    # ── Khởi chạy Node RPLidar ──────────────────────────────────────────
    rplidar_node = Node(
        package='rplidar_ros',
        executable='rplidar_composition', 
        output='screen',
        parameters=[{
            'serial_port': LaunchConfiguration('serial_port'),
            'frame_id': LaunchConfiguration('frame_id'),
            'angle_compensate': True,
            'scan_mode': 'Standard',
            'serial_baudrate': LaunchConfiguration('baud_rate') # Đã chuyển thành cấu hình động
        }]
    )

    return LaunchDescription([
        serial_port_arg,
        frame_id_arg,
        baud_rate_arg,
        rplidar_node
    ])