from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    user_major = models.CharField(max_length=45, null=False)
    user_major2 = models.CharField(max_length=45, null=True, blank=True)
    user_major3 = models.CharField(max_length=45, null=True, blank=True)


class Keyword(models.Model):
    user_id = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=45)


class Notice(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
