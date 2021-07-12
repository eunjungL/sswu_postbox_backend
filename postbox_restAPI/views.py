from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from postbox.models import User, UserInfo, Keyword, Notice
from postbox_restAPI.serializers import NoticeSerializer, KeywordSerializer, UserInfoSerializer


class UserViewSet(ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer


