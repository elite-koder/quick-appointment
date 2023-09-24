from django.contrib.auth import SESSION_KEY
from django.contrib.auth.backends import BaseBackend, ModelBackend

from users.models import User


class UserService:
    def create_user(self, username):
        user, created = User.create_new_user(username)
        return {
            "pk": user.pk,
            "username": user.username,
        }, created


# class SessionBasedBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         if isinstance(request.session.get(SESSION_KEY), int):
#             return User.get_user(request.session[SESSION_KEY])
#
#     def get_user(self, user_id):
#         return User.get_user(user_id)
