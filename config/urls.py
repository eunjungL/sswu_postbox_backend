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

    path('login/', views.LoginView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('detail/keywords/', views.KeywordDetailViewSet.as_view({'get': 'list', 'delete': 'destroy'})),

    path('update/notice/', views.UserNoticeUpdateView.as_view()),
    path('unread/notice/', views.UserNoticeUnreadCountView.as_view()),
    path('stored/notice/', views.UserNoticeStoredCountView.as_view()),
    path('destroy/notice/', views.UserNoticeDestroyView.as_view()),
]
