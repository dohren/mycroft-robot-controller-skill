from mycroft import MycroftSkill, intent_file_handler
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from pathlib import Path
import rclpy
import csv


class RobotController(MycroftSkill):
    
    goals = {}
    
    def __init__(self):
        MycroftSkill.__init__(self)

        super().__init__('pose_stamped_publisher')
        if not rclpy.ok():
            rclpy.init(args=None)
        self.node = rclpy.create_node('mycroft_ros2_skill_node')
        self.publisher = self.node.create_publisher(PoseStamped, 'goal_pose', 10)
        self.load_goals()

    def load_goals(self):    
        goal_file = Path(__file__).parent.joinpath("goals.csv")
        with open(goal_file, mode="r") as file:   
            csv_reader = csv.reader(file, delimiter=";")
            
            next(csv_reader)
            for row in csv_reader:
                goal, pos_x, pos_y, pos_z, orient_x, orient_y, orient_z, orient_w = row
                pose = {
                        "position": {
                            "x": float(pos_x),
                            "y": float(pos_y),
                            "z": float(pos_z)
                        },
                        "orientation": {
                            "x": float(orient_x),
                            "y": float(orient_y),
                            "z": float(orient_z),
                            "w": float(orient_w)
                        }
                    }
                self.goals[goal] = pose

    @intent_file_handler('controller.robot.intent')
    def handle_controller_robot(self, message):
        ort = message.data.get('ort')

        if ort in self.goals:
            goal = self.goals[ort]
            self.publish_pose_stamped(goal)
            self.speak_dialog('ich fahre los zu ' + ort, data={'ort': ort})
        else:
            self.speak_dialog('ich kenne keinen ort: ' + ort, data={'ort': ort})

    def publish_pose_stamped(self, goal):
        pose_stamped_msg = PoseStamped()
        pose_stamped_msg.header.stamp = self.node.get_clock().now().to_msg()
        pose_stamped_msg.header.frame_id = 'map'  # Set the frame ID
        pose_stamped_msg.pose.position.x = goal["position"]["x"]
        pose_stamped_msg.pose.position.y = goal["position"]["y"]
        pose_stamped_msg.pose.position.z = goal["position"]["z"]
        pose_stamped_msg.pose.orientation.x = goal["orientation"]["x"]
        pose_stamped_msg.pose.orientation.y = goal["orientation"]["y"]
        pose_stamped_msg.pose.orientation.z = goal["orientation"]["z"]
        pose_stamped_msg.pose.orientation.w = goal["orientation"]["w"]
        self.publisher.publish(pose_stamped_msg)


def create_skill():
    return RobotController()
