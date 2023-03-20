from django.db import models

from uuid import uuid4
from ..user.models import User

from lib.functions import UUIDModel, get_file_path

# Create your models here.


class Resume_Data(UUIDModel):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.TextField(max_length = 100, null=True, blank=True)
    phone_number = models.CharField(max_length=16, null=True, blank=True)
    education = models.TextField( null=True, blank=True)
    projects = models.TextField(null=True, blank=True)
    certifications = models.TextField(null=True, blank=True)
    coursework = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    position_of_responsibility = models.TextField(null=True, blank=True)
    extra_curricular = models.TextField(null=True, blank=True)
    achievements = models.TextField(null=True, blank=True)




class Resume_file(UUIDModel):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    file = models.FileField(upload_to = get_file_path)
    upload_date = models.DateTimeField(auto_now_add = True)
