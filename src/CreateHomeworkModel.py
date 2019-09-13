class CreateHomework:
    def __init__(self):
        self.homework_id = None
        self.student_id = None
        self.public_url = None

    def update_student_id(self, id):
        self.student_id = id

    def update_public_url(self, url):
        self.public_url = url

    def update_homework_id(self, id):
        self.homework_id = id

class State:
    def __init__(self):
        self.session = {}
