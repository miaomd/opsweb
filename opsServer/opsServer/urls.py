"""opsServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
# 获取用户名,密码验证通过后返回token
from rest_framework_jwt.views import obtain_jwt_token
from users.views import UserRegViewSet, UpdatePasswordView, ResetPasswordView, MyAuthValidateView, UserViews
# 引入Config
from Config.views import WebMenuViews

router = routers.DefaultRouter()
# 用户注册
router.register(r'logon', UserRegViewSet, basename='logon')
# 用户信息
router.register(r'userinfo', UserViews, basename='userinfo')
# 前端menu
router.register(r'webmenu', WebMenuViews, basename='webmenu')

urlpatterns = [
    path('admin/', admin.site.urls),
    url('api/', include(router.urls)),
    # 校验密码
    url(r'^api-token-auth', obtain_jwt_token),
    # 登录
    url(r'^login', obtain_jwt_token),
    # 根据用户名重置密码
    path('resetpwd/', ResetPasswordView.as_view()),
    # 修改密码
    path('updatepwd/', UpdatePasswordView.as_view()),
]
