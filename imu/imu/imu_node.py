import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
import csv


class ImuNode(Node):
    def __init__(self):
        super().__init__('imu_node')
        self.get_logger().info('IMU Node has been started!')
        self.publisher_ = self.create_publisher(Imu, 'imu_data', 10)
        timer_period = 1  
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.imu_data = self.read_imu_data_from_csv('imu_data.csv')
        self.data_index = 0

    def read_imu_data_from_csv(self, file_path):
        imu_data_list = []
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                imu_data_list.append(row)
        return imu_data_list

    def timer_callback(self):
        if self.data_index < len(self.imu_data):
            msg = Imu()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = 'base_link'
            msg.linear_acceleration.x = float(self.imu_data[self.data_index]['acc_x'])
            msg.linear_acceleration.y = float(self.imu_data[self.data_index]['acc_y'])
            msg.linear_acceleration.z = float(self.imu_data[self.data_index]['acc_z'])
            msg.angular_velocity.x = float(self.imu_data[self.data_index]['ang_x'])
            msg.angular_velocity.y = float(self.imu_data[self.data_index]['ang_y'])
            msg.angular_velocity.z = float(self.imu_data[self.data_index]['ang_z'])
            msg.orientation.x = float(self.imu_data[self.data_index]['orient_x'])
            msg.orientation.y = float(self.imu_data[self.data_index]['orient_y'])
            msg.orientation.z = float(self.imu_data[self.data_index]['orient_z'])
            msg.orientation.w = float(self.imu_data[self.data_index]['orient_w'])
            self.publisher_.publish(msg)
            self.get_logger().info('Published IMU data from index: %d' % self.data_index)
            self.data_index += 1
        else:
            self.get_logger().info('No more IMU data to publish.')


def main(args=None):
    rclpy.init(args=args)
    node = ImuNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()