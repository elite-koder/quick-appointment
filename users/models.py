from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    @classmethod
    def create_new_user(cls, username):
        return cls.objects.get_or_create(username=username, defaults={"first_name": "", "last_name": "", "email": ""})

    @classmethod
    def get_user_by_username(cls, username):
        return cls.objects.get(username=username)

    @classmethod
    def get_user(cls, pk):
        return cls.objects.get(pk=pk)

    def get_session_auth_hash(self):
        return "qwerty"
