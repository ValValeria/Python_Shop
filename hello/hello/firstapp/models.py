from django.db import models
from django.db import models
from django.contrib.auth.models import (
   BaseUserManager,AbstractBaseUser
)
from django.conf import settings
from .perm import Perm

class Role(models.Model):
       update=models.BooleanField(default=True)
       update_all=models.BooleanField(default=False)
       create_posts=models.BooleanField(default=True)
       show_profile_all=models.BooleanField(default=False)
       

#https://docs.djangoproject.com/en/3.0/topics/db/managers/#django.db.models.Manager
#https://docs.djangoproject.com/en/3.0/topics/auth/customizing/
class MyUserManager(BaseUserManager):
    def create_user(self,username, email, password=None,role=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        

        user = self.model(
            email=email,
            username=username,
            password=password,
            role=role
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=email,
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user






class Post(models.Model):
    time=models.DateTimeField()
    users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
   # picture = models.ImageField(upload_to = 'pictures')
    title=models.CharField(max_length=50)
    content=models.CharField(max_length=600)
    

class Category(models.Model):
    post = models.OneToOneField(Post, on_delete = models.DO_NOTHING,related_name="category1")
    furnish=models.BooleanField(default=False)
    services=models.BooleanField(default=False)
    cars=models.BooleanField(default=False)

class Images(models.Model):
    post=models.OneToOneField(Post, on_delete = models.DO_NOTHING,related_name="images1")
    images=models.CharField(max_length=500)


class Products(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    count_of = models.IntegerField()

class MyUser(AbstractBaseUser):
       email=models.EmailField(max_length=30)
       password=models.CharField(max_length=20)
       username=models.CharField(max_length=20)
       role=models.ForeignKey(Role,on_delete = models.DO_NOTHING)
       is_active = models.BooleanField(default=True)
       is_admin = models.BooleanField(default=False)
       objects=MyUserManager()
       USERNAME_FIELD = 'id'
       EMAIL_FIELD='email'
       products_u = models.ManyToManyField(Post, through='Products',related_name="buyers")

       def __str__(self):
           return self.email
       
       def has_perm(self,perm,obj=None):
           return Perm().can(perm,self,obj)
       
       def get_user_permissions(self):
           return Perm()
       @property
       def is_staff(self):
           return self.is_admin



