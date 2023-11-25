from mycroft import MycroftSkill, intent_file_handler


class RobotController(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('controller.robot.intent')
    def handle_controller_robot(self, message):
        ort = message.data.get('ort')

        self.speak_dialog('controller.robot', data={
            'ort': ort
        })


def create_skill():
    return RobotController()

