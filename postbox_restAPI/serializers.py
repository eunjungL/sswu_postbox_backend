from abc import ABC

from rest_framework import serializers, status
from postbox.models import UserInfo, Notice, Keyword, UserNotice
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import json


class UserInfoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserInfo
        fields = "__all__"

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])
        user.save()

        user_info = UserInfo.objects.create(
            user=user,
            user_major=validated_data['user_major'],
            user_major2=validated_data['user_major2'],
            user_major3=validated_data['user_major3']
        )
        user_info.save()

        return user_info

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['user'] = instance.user.username

        return ret


class UserInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = "__all__"
        depth = 1


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = "__all__"


class UserNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotice
        fields = "__all__"
        depth = 1

    def to_representation(self, instance):
        ret = super(UserNoticeSerializer, self).to_representation(instance)
        ret['user'] = instance.user.username

        return ret

    def create(self, validated_data):
        keywords = Keyword.objects.filter(user=self.context['request'].user)

        notices = []
        for keyword in keywords:
            for notice in Notice.objects.filter(title__icontains=keyword):
                notices.append(notice)

        user_notices = []
        for notice in notices:
            user_notice, created = UserNotice.objects.get_or_create(
                   user=self.context['request'].user,
                   notice=notice
            )
            if created:
                user_notice.save()
                user_notices.append(user_notice)
            else:
                user_notice.notice.title = "duplicate"
                user_notices.append(user_notice)

        return user_notices[0]


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['user'] = instance.user.username

        return ret

    def create(self, validated_data):
        keyword, created = Keyword.objects.get_or_create(
            user=self.context['request'].user,
            keyword=validated_data['keyword']
        )

        if created:
            keyword.save()
        else:
            keyword.keyword = "duplicate"
            return keyword

        return keyword


class LoginSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(LoginSerializer, cls).get_token(user)

        token['username'] = user.username
        return token
