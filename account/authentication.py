from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
class EmailAuthentication(object):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except:
            return None
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except:
            return None
