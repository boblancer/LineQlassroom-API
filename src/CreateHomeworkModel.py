class CreateHomework:
    def __init__(self):
        self.student_id = None
        self.public_url = None
        self.imageUrl

    def update_student_id(self, id):
        self.student_id = id

    def update_public_url(self, url):
        self.public_url = url