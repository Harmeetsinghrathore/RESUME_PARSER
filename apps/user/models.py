from django.db import models
from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser

from .managers import UserManager


# Create your models here.

class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True,default = uuid4, editable = False)   
    firstname = models.CharField(max_length = 256, default = 'testfirst')
    lastname = models.CharField(max_length = 256, default = 'testlast')
    email = models.EmailField(max_length = 254, unique = True)
    active  = models.BooleanField(default = False)
    normal_user = models.BooleanField(default = False)
    admin = models.BooleanField(default = False)
    staff = models.BooleanField(default = False)
    otp = models.IntegerField(null = True)
    created_date = models.DateField(auto_now_add = True, null = True)
    mobile = models.CharField(max_length = 15, unique = False, blank = True, null = True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['firstname','lastname']

    def __str__(self):
        return self.email+" - "+str(self.id)

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True

    def get_permissions(self):

        permissions = {
            'is_admin': str(self.admin).lower(),
            'is_staff': str(self.staff).lower(),
            'normal_user': str(self.normal_user).lower(),
            'is_active': str(self.active).lower()
        }

        return permissions
