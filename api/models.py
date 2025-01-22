from django.db import models
import datetime


class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    createdAt = models.DateTimeField(auto_now_add=True)

    settings = models.JSONField(
        default=lambda: {'apiKey': '', 'language': 'English'})

    def __init__(self, username, email, password, createdAt=None):
        self.username = username
        self.email = email
        self.password = password
        self.createdAt = createdAt or datetime.datetime.now()

    def __str__(self):
        return self.username


""" class Language:
    def __init__(self, name):
        self.name = name

class Style:
    def __init__(self, name, description):
        self.name = name
        self.description = description """
