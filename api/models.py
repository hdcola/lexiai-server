import datetime


class User:
    def __init__(self, username, email, password, created_at=None):
        self.username = username
        self.email = email
        self.password = password
        self.created_at = created_at or datetime.datetime.now()


""" class Language:
    def __init__(self, name):
        self.name = name

class Style:
    def __init__(self, name, description):
        self.name = name
        self.description = description """
