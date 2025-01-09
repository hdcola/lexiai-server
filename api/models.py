import datetime


class User:
    def __init__(self, username, email, password, createdAt=None):
        self.username = username
        self.email = email
        self.password = password
        self.createdAt = createdAt or datetime.datetime.now()