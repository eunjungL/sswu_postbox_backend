from rest_framework import serializers
from postbox.models import UserInfo, Notice, Keyword
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User


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


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = "__all__"


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = "__all__"
