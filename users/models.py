import jwt

from datetime import datetime, timedelta
from django.db import models
from django.conf import settings 
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager, PermissionsMixin
)

class UserManager(BaseUserManager):
   
    def create_user(self, email, first_name, last_name, password=None):
       
        if last_name is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email), first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, first_name, last_name, password):
        
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    update_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email


    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.last_name

    def get_short_name(self):
        return self.last_name

    def _generate_jwt_token(self):

        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'email': self.email,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

