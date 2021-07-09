from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserInfo(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    user_major = models.CharField(max_length=45)
    user_major2 = models.CharField(max_length=45, null=True)
    user_major3 = models.CharField(max_length=45, null=True)

class Keyword(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    keyword = models.CharField(max_length=45)

class Notice(models.Model):
    title = models.CharField()
    url = models.URLField()
