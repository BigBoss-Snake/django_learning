import jwt

from datetime import datetime, timedelta
from django.db import models
from django.conf import settings 
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager, PermissionsMixin
)

class UserManager(BaseUserManager):
   
    def create_user(self, username, email, password=None):
       
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=40)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    update_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    @property
    def __str__(self):
        return self.email


    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.last_name + self.first_name

    def get_short_name(self):
        return self.first_name 

    def _generate_jwt_token(self):

        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

