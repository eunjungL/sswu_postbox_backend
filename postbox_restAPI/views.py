from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from postbox.models import User, UserInfo, Keyword, Notice, UserNotice
from postbox_restAPI.serializers import (NoticeSerializer, KeywordSerializer, UserInfoSerializer,
                                         LoginSerializer, UserNoticeSerializer, UserInfoUpdateSerializer)
from rest_framework import permissions, status, generics, filters
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


# User
class UserViewSet(ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    pagination_class = None


class UserDetailView(generics.ListAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoUpdateSerializer
    pagination_class = None

    # Get Method 유저 상세 정보 가져오기
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class UserUpdateView(generics.UpdateAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoUpdateSerializer

    # PATCH Method 유저 정보 수정(학과 수정)
    def partial_update(self, request, *args, **kwargs):
        queryset = self.queryset.get(user=self.request.user)
        serializer = self.serializer_class(queryset, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer


# Keyword
class KeywordViewSet(ModelViewSet):
    # POST Method 키워드 생성
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class KeywordDetailViewSet(ModelViewSet):
    # 키워드 검색
    search_fields = ['keyword']
    filter_backends = (filters.SearchFilter,)
    pagination_class = None

    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # GET Method 각 유저별 키워드 목록 가져오기
    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)

        return query_set

    # DELETE Method 각 유저별 키워드 삭제하기
    def destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        keyword_get = self.request.query_params.get('keyword')

        queryset = queryset.filter(keyword=keyword_get)
        self.perform_destroy(queryset)

        return Response(status=status.HTTP_204_NO_CONTENT)


# Notice
class NoticeViewSet(ModelViewSet):
    # Crawling 해서 얻은 전체 공지사항 저장 및 조회
    # 공지사항 제목으로 검색
    search_fields = ['title']
    filter_backends = (filters.SearchFilter,)

    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserNoticeViewSet(ModelViewSet):
    # 공지사항 제목으로 검색
    search_fields = ['notice__title']
    filter_backends = (filters.SearchFilter,)
    queryset = UserNotice.objects.all()
    serializer_class = UserNoticeSerializer

    # GET Method 각 유저의 키워드 별 공지사항 최신순으로 가져오기
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-notice__date')


class UserNoticeDestroyView(generics.DestroyAPIView):
    queryset = UserNotice.objects.all()
    serializer_class = UserNoticeSerializer

    # DELETE Method 유저의 키워드 삭제 시, 유저 키워드 별 공지사항 CASCADE
    def destroy(self, request, *args, **kwargs):
        queryset = self.queryset
        keyword = self.request.query_params.get('keyword')

        queryset = queryset.filter(notice__title__icontains=keyword)
        self.perform_destroy(queryset)

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserNoticeUpdateView(generics.UpdateAPIView):
    queryset = UserNotice.objects.all()
    serializer_class = UserNoticeSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]

    # PATCH Method 읽음 표시 수정 / 보관, 보관 취소 표시 수정
    def partial_update(self, request, *args, **kwargs):
        queryset = self.queryset.filter(user=self.request.user)
        queryset = queryset.get(notice__title=self.request.data['title'])
        serializer = self.serializer_class(queryset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class UserNoticeUnreadCountView(generics.ListAPIView):
    queryset = UserNotice.objects.all()
    serializer_class = UserNoticeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # GET Method 안 읽은 공지사항만 가져오기
    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        queryset = queryset.filter(read=False)
        return queryset


class UserNoticeStoredView(generics.ListAPIView):
    queryset = UserNotice.objects.all()
    serializer_class = UserNoticeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = None

    # GET Method 보관한 공지사항만 최신순으로 가져오기
    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        queryset = queryset.filter(store=True)
        return queryset.order_by('-notice__date')

