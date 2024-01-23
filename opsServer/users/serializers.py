from rest_framework import serializers
# 引入django自带的用户系统
from django.contrib.auth import get_user_model
# from django.contrib.auth import l
from django.contrib import auth

# 将get_user_model赋值给User方便调用
User = get_user_model()


# 注册用户
class UserRegSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        pwd = validated_data["password"]
        user.set_password(pwd)
        user.save()
        return user

    class Meta:
        model = User
        fields = ["name", 'username', 'password', "role"]


# from .models import UserProfile, myauth
from .models import UserProfile

# 返回用户信息
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["name", "username", "job_num", "role"]


# 返回角色权限
# class MyAuthSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = myauth
#         fields = ["level", "authlist", "remarks"]
