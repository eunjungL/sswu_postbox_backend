from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from postbox.models import User, UserInfo, Keyword, Notice
from postbox_restAPI.serializers import NoticeSerializer, KeywordSerializer, UserInfoSerializer

class UserViewSet(ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
