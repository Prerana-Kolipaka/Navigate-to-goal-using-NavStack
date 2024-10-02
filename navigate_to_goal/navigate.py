import rclpy
from rclpy.node import Node
from builtin_interfaces.msg import Time
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action._navigate_to_pose import NavigateToPose_FeedbackMessage
import time

class GoalPublisher(Node):

    def __init__(self):
        super().__init__('goal_publisher')
        self.publisher = self.create_publisher(PoseStamped, '/goal_pose', 10)
        self.subscriber = self.create_subscription(NavigateToPose_FeedbackMessage, '/navigate_to_pose/_action/feedback', self.goal_callback,10) 
        
        #timer_period = 0.5  # seconds
        #self.timer = self.create_timer(timer_period, self.timer_callback)
        #self.i = 0
        self.pos1_flag = False
        self.pos2_flag = False
        self.pos3_flag = False
        self.pos1= PoseStamped()
        self.pos2= PoseStamped()
        self.pos3= PoseStamped()
        #self.pos1 = self.set_point([2.55, -0.956, 0.0, 0.0,0.0,0.0,1.0])
        self.pos1 = self.set_point([1.52, -0.77, 0.0, 0.0,0.0,0.0,1.0])        
        self.cur_pos = PoseStamped()
        self.cur_pos = self.pos1
        self.get_logger().info('done init')
        timer_period = 1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        

    def timer_callback(self):
    	self.publisher.publish(self.cur_pos)
    	
        
    def set_point(self, goalPos):
        goal_pose = PoseStamped()
        goal_pose.header.frame_id = 'map'
        goal_pose.header.stamp = Time(sec=0,nanosec=0)
        goal_pose.pose.position.x = goalPos[0]
        goal_pose.pose.position.y = goalPos[1]
        goal_pose.pose.position.z = goalPos[2]
        goal_pose.pose.orientation.x = goalPos[3]
        goal_pose.pose.orientation.y = goalPos[4]
        goal_pose.pose.orientation.z = goalPos[5]
        goal_pose.pose.orientation.w = goalPos[6]
        #self.publisher.publish(goal_pose)
	          
        return goal_pose
	  
    def goal_callback(self, msg):
        feedback_cur_pos = msg.feedback.current_pose
        dist = ((feedback_cur_pos.pose.position.x-self.cur_pos.pose.position.x)**2+(feedback_cur_pos.pose.position.y-self.cur_pos.pose.position.y)**2)**0.5
        self.get_logger().info('Distance to goal %f' % dist)
        if dist<=0.25:
            
            if not self.pos1_flag:        	    
                self.pos1_flag = True
                time.sleep(5)
                self.pos2 = self.set_point([4.52, 1.016, 0.0, 0.0,0.0,0.0,1.0])        
                self.cur_pos = self.pos2     	        
                self.get_logger().info('First goal reached')
                
                
            elif not self.pos2_flag:        	   
                self.pos2_flag = True
                #self.publisher.publish(self.pos3) 
                time.sleep(5)
                self.pos3 = self.set_point([3.58, -0.736, 0.0, 0.0,0.0,0.0,1.0])    
                self.cur_pos = self.pos3   	        
                self.get_logger().info('Second goal reached')
                
                
            elif not self.pos3_flag:        	    
                self.pos3_flag = True
                self.get_logger().info('Final goal reached')
        	        
  

def main(args=None):
    rclpy.init(args=args)

    goal_publisher = GoalPublisher()

    rclpy.spin(goal_publisher)
    #goal_publisher.publisher.publish(goal_publisher.pos1)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
