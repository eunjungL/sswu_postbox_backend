from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from postbox.models import User, UserInfo, Keyword, Notice
from postbox_restAPI.serializers import (NoticeSerializer, KeywordSerializer, UserInfoSerializer,
                                         MyTokenObtainPariSerializer)
from rest_framework import permissions, status, generics
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView


class UserViewSet(ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MyTokenObtainPariSerializer


class KeywordViewSet(ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class KeywordDetailViewSet(ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)

        return query_set

    def destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        keyword_get = self.request.query_params.get('keyword')

        queryset = queryset.filter(keyword=keyword_get)
        self.perform_destroy(queryset)

        return Response(status=status.HTTP_204_NO_CONTENT)

