from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


# User
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    user_major = models.CharField(max_length=45, null=False)
    user_major2 = models.CharField(max_length=45, null=True, blank=True)
    user_major3 = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return self.user.username


# Keyword
class Keyword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    keyword = models.CharField(max_length=45)

    def __str__(self):
        return self.keyword


# Notice
class Notice(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now())
    url = models.URLField()

    def __str__(self):
        return self.title


class UserNotice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, null=True)
    store = models.BooleanField(default=False)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.notice.title