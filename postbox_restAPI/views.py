from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from postbox.models import User, UserInfo, Keyword, Notice
from postbox_restAPI.serializers import (NoticeSerializer, KeywordSerializer, UserInfoSerializer,
                                         MyTokenObtainPariSerializer)
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView


class UserViewSet(ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = [permissions.IsAuthenticated]


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MyTokenObtainPariSerializer
