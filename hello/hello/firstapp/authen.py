from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

class MyBackend(BaseBackend):
    def authenticate(self,email=None, password=None):
         try:
             user=User.objects.get(email=email)
             if user.check_password(password):
                 raise User.DoesNotExist
         except User.DoesNotExist:
             return None
         return user 
