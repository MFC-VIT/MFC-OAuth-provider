from django.db import models
from django.contrib.auth.models import (AbstractUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, username, email, phone_number,reg_no, password=None):
        if username is None:
            raise TypeError('Users should have a name')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email), phone_number=phone_number, reg_no = reg_no)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Password should not be none')

        phone_number = '1234567890'
        reg_no = '19BIT0000'
        user = self.create_user(username, email, phone_number, reg_no, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractUser):
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    phone_number = PhoneNumberField()
    reg_no = models.CharField(max_length=10,default='19BIT0000')
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    otp = models.IntegerField(blank=True,null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
