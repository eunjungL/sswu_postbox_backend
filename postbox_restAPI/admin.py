from django.contrib import admin
from postbox.models import UserInfo, Keyword, Notice, UserNotice

admin.site.register(UserInfo)
admin.site.register(Keyword)
admin.site.register(Notice)
admin.site.register(UserNotice)
# Register your models here.
