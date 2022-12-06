from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id):
        self.email, self.password = id.split(' ')
        self.id = id