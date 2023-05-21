import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry as Odometry
from time import sleep
from tf_transformations import euler_from_quaternion
import math

MAX_DIFF = 0.1

global path
path = [
    [-1.0, 0.0], 
    [-1.0, 1.0], 
    [0.0, 1.0], 
    [0.0, 0.0]  
]

# Classe que cria o nó
class TurtleController(Node):
    def __init__(self, control_period=0.05):
        super().__init__('turtlecontroller')
        self.main_array = 1

        self.odom = Odometry()
        self.point = self.odom.pose.pose
        self.x_point = self.point.position.x
        self.y_point = self.point.position.y

        self.x_point = path[(self.main_array - 1)][0]
        self.y_point = path[(self.main_array - 1)][1]

        self.dom_point = Odometry()
        self.setpoint = self.dom_point.pose.pose
        self.x_setpoint = self.setpoint.position.x
        self.y_setpoint = self.setpoint.position.y

        self.x_setpoint = path[self.main_array][0]
        self.y_setpoint = path[self.main_array][1]
        print(f'x={self.x_point}, y={self.y_point}')
        print(f'x={self.x_setpoint}, y={self.y_setpoint}')
        
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(Odometry, '/odom', self.pose_callback, 10)
        self.control_timer = self.create_timer(timer_period_sec = control_period, callback = self.control_callback)

    def pose_callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        angulo = msg.pose.pose.orientation

        _, _, self.theta = euler_from_quaternion([angulo.x, angulo.y, angulo.z, angulo.w]) 

        self.x_point = x
        self.y_point = y

        self.get_logger().info(f"Atual x={round(x, 2)}, y={round(y, 2)}, theta={round(math.degrees(self.theta), 2)}")

    def control_callback(self):
        msg = Twist()

        self.x_setpoint = path[self.main_array][0] 
        self.y_setpoint = path[self.main_array][1]
        diff_x = self.x_setpoint - self.x_point 
        diff_y = self.y_setpoint - self.y_point
        mainly_angle = math.atan2(diff_y, diff_x) 
        angulo_diff = mainly_angle - self.theta 

        print(f"Diferença em x={round(abs(diff_x), 2)}, Diferença em y={round(abs(diff_y), 2)}, Diferença no angulo={round(abs(angulo_diff), 2)}")
        
        if (abs(diff_x) < MAX_DIFF and abs(diff_y) < MAX_DIFF):
            self.main_array += 1

        if abs(angulo_diff) > (MAX_DIFF -0.05):
            msg.linear.x = 0.0
            msg.angular.z = 0.2 if angulo_diff > 0 else -0.2
        elif abs(diff_x) > MAX_DIFF:
            msg.linear.x = 0.2
        
        if self.main_array == (len(path) - 1):
            msg.linear.x = 0.0
            msg.linear.y = 0.0
            msg.angular.z = 0.0
            self.publisher.publish(msg)
            self.get_logger().info("Chegou ao seu destino")
            exit()
        self.publisher.publish(msg)
            
def main(args=None):
    rclpy.init(args=args)
    tc = TurtleController()
    rclpy.spin(tc)
    tc.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()