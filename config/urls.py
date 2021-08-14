"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from postbox_restAPI import views
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'keywords', views.KeywordViewSet)
router.register(r'notice', views.NoticeViewSet)
router.register(r'userNotice', views.UserNoticeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),

    # 유저 상세 정보 가져오기 / 유저 정보 수정
    path('detail/user/', views.UserDetailView.as_view()),
    path('update/user/', views.UserUpdateView.as_view()),

    # Login
    path('login/', views.LoginView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 유저 별 키워드 목록, 검색, 삭제
    path('detail/keywords/', views.KeywordDetailViewSet.as_view({'get': 'list', 'delete': 'destroy'})),

    # 공지사항 수정(읽음, 보관상태) / 안읽은 공지사항 가져오기 / 보관된 공지사항 가져오기 / 키워드 삭제 시 공지사항 CASCADE
    path('update/notice/', views.UserNoticeUpdateView.as_view()),
    path('unread/notice/', views.UserNoticeUnreadCountView.as_view()),
    path('stored/notice/', views.UserNoticeStoredView.as_view()),
    path('destroy/notice/', views.UserNoticeDestroyView.as_view()),
]
