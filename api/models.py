import datetime


class User:
    def __init__(self, username, email, password, createdAt=None):
        self.username = username
        self.email = email
        self.password = password
        self.createdAt = createdAt or datetime.datetime.now()


""" class Language:
    def __init__(self, name):
        self.name = name

class Style:
    def __init__(self, name, description):
        self.name = name
        self.description = description """
