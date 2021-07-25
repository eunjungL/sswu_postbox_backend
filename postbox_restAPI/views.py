from rest_framework.viewsets import ModelViewSet
from postbox.models import User, UserInfo, Keyword, Notice, UserNotice
from postbox_restAPI.serializers import (NoticeSerializer, KeywordSerializer, UserInfoSerializer,
                                         LoginSerializer, UserNoticeSerializer)
from rest_framework import permissions, status, generics, filters
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class UserViewSet(ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer


class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer


class KeywordViewSet(ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class KeywordDetailViewSet(ModelViewSet):
    search_fields = ['keyword']
    filter_backends = (filters.SearchFilter,)

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


class NoticeViewSet(ModelViewSet):
    search_fields = ['title']
    filter_backends = (filters.SearchFilter,)

    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserNoticeViewSet(ModelViewSet):
    queryset = UserNotice.objects.all()
    serializer_class = UserNoticeSerializer


class UserNoticeUpdateView(generics.UpdateAPIView):
    queryset = UserNotice.objects.all()
    serializer_class = UserNoticeSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]

    def partial_update(self, request, *args, **kwargs):
        queryset = UserNotice.objects.get(notice__title=self.request.data['title'])
        serializer = self.serializer_class(queryset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class UserNoticeUnreadCountView(generics.ListAPIView):
    queryset = UserNotice.objects.all()
    serializer_class = UserNoticeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset.filter(read=False)
        return queryset


class UserNoticeStoredCountView(generics.ListAPIView):
    queryset = UserNotice.objects.all()
    serializer_class = UserNoticeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset.filter(store=True)
        return queryset

