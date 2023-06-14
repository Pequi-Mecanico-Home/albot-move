import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range


class MovingAround(Node):

    def __init__(self):
        super().__init__('moving_around')

        self.sonar_range = 0

        self.subscription = self.create_subscription(
            Range,
            'distance/front_right_sonar',
            self.callback_sonar,
            10)
        
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.callback_timer)
        self.i = 0


    def callback_timer(self):
            
        self.vel = Twist()
        if self.sonar_range > 0.5:
            self.vel.linear.x = 0.25
            self.vel.angular.z = 0.0
        else:
            self.vel.linear.x = 0.0
            self.vel.angular.z = 0.2
        self.publisher_.publish(self.vel)

        # self.get_logger().info(f'Running: {msg.linear.x}')
        self.i += 1

    def callback_sonar(self, msg):
        self.sonar_range = msg.range



def main(args=None):
    rclpy.init(args=args)

    moving_around = MovingAround()

    try:
        rclpy.spin(moving_around)

    finally:
       
        moving_around.vel = Twist()  # Velocidade zerada
        moving_around.publisher_.publish(moving_around.vel)
        moving_around.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()