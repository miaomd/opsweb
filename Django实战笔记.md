# 安装工具

1. 安装python

2. 安装pycharm

3. 安装djiango

   ```
   #安装djiango
   pip install django
   #查看已安装的djiango版本
   python -m django --version
   ```

4. 其他依赖

   ```
   PyJWT
   djangorestframework
   djangorestframework-jwt
   ```

# 创建djiango项目TCweb

- windows

  在d盘根目录

  ```
  win+r 运行cmd
  cd d:\
  django-admin.exe startproject TCweb
  ```

- Linux

  cd 到项目目录

  ```
  django-admin startproject TCweb
  ```

# IP放行

项目settings.py

```
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'your_ip or 域名']
```

# django实现跨域

安装依赖

```
pip install django-cors-headers
```

根目录 setting.py 的 INSTALLED_APPS 内增加 corsheaders

```
INSTALLED_APPS = [
    'rest_framework',
    'corsheaders',
]
```

根目录 setting.py 的 MIDDLEWARE 第三行，增加跨域设置

```
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # 跨域设置
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

根目录 setting.py 的最后，空白位置，增加允许站外请求代码

```
#允许站外请求
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = ('*')
```

# 后端（django）API

安装依赖

```
pip install djangorestframework
pip install markdown      
pip install django-filter 
#drf+jwt实现token
pip install djangorestframework-jwt
```

rest_framework 引入到根目录的setting.py内

```
INSTALLED_APPS = [
    'HuanJingGuanLi.apps.HuanjingguanliConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework'
]
```

根目录 settings.py 配置drf（setting.py 内 DATABASES 后，添加以下内容）

```
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
```

在组件 HuanJingGuanLi 文件夹内，新增序列化文件serializers.py，并写入以下内容

```
from rest_framework import serializers
from .models import huanjing
class HuanjingSerializer(serializers.ModelSerializer):
    class Meta:
        model = huanjing
        fields = ['sys', 'SIT1', 'SIT2','SIT3','SIT4','remarks']
```

修改 HuanJingGuanLi  目录下的views.py，写入以下内容

```
from django.shortcuts import render
# Create your views here.
from .serializers import HuanjingSerializer
from .models import huanjing
# Create your views here.
from rest_framework import viewsets, mixins
class HuanjingViews(viewsets.ModelViewSet):
    serializer_class = HuanjingSerializer
    def get_queryset(self):
        return huanjing.objects.all()
```

配置路由，修改根目录的 urls.py 内容

```django
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url,include
from rest_framework import routers
router = routers.DefaultRouter()
from HuanJingGuanLi.views import HuanjingViews

router.register(r'huanjing',HuanjingViews,basename='huanjing')

#获取用户名密码验证通过后返回token
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url('admin/', admin.site.urls),
    url('api/', include(router.urls)),
    url(r'^api-token-auth',obtain_jwt_token),
    path('api-auth/', include('rest_framework.urls',namespace='rest_framework')),
]
```

访问，访问以下网址即可获取接口提供的数据

http://127.0.0.1:8000/api/huanjing/

ps：

http://127.0.0.1:8000/api/	获取所有后端API

http://127.0.0.1:8000/api-token-auth 前端通过post请求实现用户登录验证并获取token

# 启动项目TCweb

## 终端运行

```
#进入项目TCweb目录下
cd D:\TCweb
#启动项目
	#只对本机提供服务
		python manage.py runserver
	#对外提供服务
		python manage.py runserver 0.0.0.0:8000
	#后台持久化运行
		nohup python manage.py runserver 0.0.0.0:8000 &
#manage.py是运行各种django命令的文件，使用该命令会生成一个python自带的数据库文件db.sqlite3
```

## pycharm debug调试运行

- 运行→调试→编辑配置→新增→python
- 名字自定义
- 脚本路径：项目下manage.py的路径
- 形参：runserver 0.0.0.0:8000
- 应用→调试

# 项目默认网址

```
#打开浏览器。输入以下网址，就能看到django自带的web应用界面了
http://127.0.0.1:8000/
```

# 停止项目服务

```
ctrl+c
#停止后，需要重启服务
python manage.py runserver
```

# 对接数据库

修改项目同名目录下的setting.py文件，具体如下

```
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '数据库名',
        'HOST': '数据库IP',
        'PORT': '3306',
        'USER': '用户名',
        'PASSWORD': '密码',
    }
}
```

## 异常处理

启动项目运行正常即为配置正常。如果报错见招拆招，以下是我遇见的问题

报错信息：

```
django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module.
Did you install mysqlclient?
```

解决方案：
修改settings.py同级目录下的__init__.py ，增加以下内容

```
import pymysql
pymysql.install_as_MySQLdb()
```

报错信息 

```
File "C:\python36\lib\site-packages\django\db\backends\mysql\operations.py", line 146, in last_executed_query
      query = query.decode(errors='replace')
  AttributeError: 'str' object has no attribute 'decode'
```

解决方案：

找到报错的这个文件C:\python36\lib\site-packages\django\db\backends\mysql\operations.py，修改query = query.decode(errors='replace')为query = query.encode(errors='replace'),如下

```
def last_executed_query(self, cursor, sql, params):
        # With MySQLdb, cursor objects have an (undocumented) "_executed"
        # attribute where the exact query sent to the database is saved.
        # See MySQLdb/cursors.py in the source distribution.
        query = getattr(cursor, '_executed', None)
        if query is not None:
            # query = query.decode(errors='replace')
            query = query.encode(errors='replace')
        return query
```

## 数据写入数据库

- 通过model对数据库表进行变更后需要执行该操作，将变更同步到数据库

- 功能数据写入MySQL（在python中记录变更，数据库此时并未变更）

  ```
  python manage.py makemigrations
  
  ps:
  如果只想讲某个模块的修改写入数据库，可以在 makemigrations 后面写上项目名称
  ```

- 数据引入，更新MySQL

  ```
  python manage.py migrate
  ```

# Pycharm连接数据库

pycharm的简单配置

专业版pycharm直接使用database工具

社区版：file→setting→plugins，搜索database，安装database navigator

社区版离线安装database navigator：

```
联网电脑先安装然后找到，安装文件DBNavigator，复制到离线电脑的相应位置。
路径：C:\Users\用户名\AppData\Roaming\JetBrains\PyCharmCE2020.2\plugins
```

## 连接数据库时报错及解决方案

错误信息

```
You must configure either the server or JDBC driver (via the 'serverTimezone' configuration property) to use a more specifc time zone value if you want to utilize time zone support.
```

方案：在MySQL的命令行工具（MySQL 5.7 Command Line Client）执行以下语句后，重新连接数据库 

```
set global time_zone='+8:00';
```

# 建立用户系统

启用Django自带的用户管理模块

## 创建用户模块

在项跟目录下输入以下命令

```
python manage.py startapp users
```

## 修改用户模块

如果要在Django自带模型的基础上增加表字段，可以修改models.py

```
from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    """用户系统"""
    LEVEL=(
        ('user','用户'),
        ('manager','中心主任'),
        ('admin','管理员'),
        ('SuperAdmin','超级管理员')
    )
    name=models.CharField(max_length=32,null=True,blank=True,verbose_name="姓名")
    lgname=models.CharField(max_length=32,null=True,blank=True,verbose_name="登录名")
    usernum=models.CharField(max_length=32,null=True,blank=True,verbose_name="工号")
    level=models.CharField(choices=LEVEL,max_length=32,null=True,blank=True,verbose_name="用户类型")
```

添加定义用户验证

在 setting.py 内 ALLOWED_HOSTS 下一行增加（否则使用djiango自带的用户验证）

```
AUTH_USER_MODEL = 'users.UserProfile'
```

在 setting.py 内 INSTALLED_APPS 添加一行

```
'users.apps.UsersConfig'
```

功能数据写入MySQL

```
python manage.py makemigrations
```

数据引入，更新MySQL

```
python manage.py migrate
```

# 创建超级管理员

- 创建

  ```
  python manage.py createsuperuser
  ```

- 使用超级管理员，登录django后管平台

  ```
  http://127.0.0.1:8000/admin
  ```

- 一般情况下需要先创建user再创建超级管理员，如果先创建了管理员，在创建user时会报错

  ```
  django.db.migrations.exceptions.InconsistentMigrationHistory: Migration admin.0001_initial is applied before its dependency users.0001_initial on database 'default'.
  ```

  因为管理员也是用户，如果创建了之后在修改用户表的字段，会产生冲突。可以使用如下方法解决：

  1. 注释掉所有关于admin的引用，settings.py中的INSTALLED_APPS，urls.py中的import和path，users中的admin.py中的import

  2. 重新执行

     ```
     python manage.py makemigrations
     python manage.py migrate
     ```

  3. 将第一步的所有注释取消
  
  4. 因为修改了用户模块，用户信息的记录使用了不同的表（Django默认使用的auth_，修改后的用户表默认使用user前缀），所以修改引用模块前创建的超级管理员失效，重新执行创建管理员的命令

# 用户管理

## 新建serializers.py

user模块下serializers.py，写入以下代码

```python
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


from .models import UserProfile, myauth


# 返回用户信息
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["name", "username", "job_num", "role"]


# 返回角色权限
class MyAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = myauth
        fields = ["level", "authlist", "remarks"]

```

## 重定义JWT验密后返回的内容

- 重写jwt_response_payload_handler

  \users\utils.py（新建）

  ```python
  from rest_framework_jwt.utils import jwt_response_payload_handler
  from .serializers import UserInfoSerializer
  
  def jwt_response_payload_handler(token, user=None, request=None):
      return {
          'token': token,
          'user': UserInfoSerializer(user, context={'request': request}).data
      }
  ```

- 设置验密后返回重定义内容

  /settings.py，最后增加以下内容

  ```
  JWT_AUTH = {
      # """设置处理时使用的函数，就是上一步我们自己定义的那一个"""
      'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.utils.jwt_response_payload_handler'
  }
  ```

  

## 编辑视图文件

user下的views.py

```python
from django.shortcuts import render
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegSerializer, MyAuthSerializer, UserInfoSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import myauth
from ZiYuanChi.models import tester
from django.http import HttpResponse
import json
import re

User2 = get_user_model()


# Create your views here.

class UserViews(viewsets.ModelViewSet):
    queryset = User2.objects.all()
    serializer_class = UserInfoSerializer

    def get_queryset(self):
        my_res = {"myState": "success", "myDesc": ""}
        try:
            my_type = self.request.GET["type"]
            if my_type == "namedict":
                my_team = "测试中心"
                re_list = []
                re_queryset = User2.objects.filter(team=my_team).order_by("username")
                val_list = re_queryset.values()
                for val in val_list:
                    re_list.append({"username": val["username"], "name": val["name"]})
                my_res["myState"] = "success"
                my_res["myDesc"] = re_list
        except Exception as e:
            my_res["myState"] = "fail"
            my_res["myDesc"] = str(e)
            return HttpResponse(json.dumps(my_res))
        else:
            return HttpResponse(json.dumps(my_res))

    def create(self, request, *args, **kwargs):
        my_res = {"myState": "success", "myDesc": ""}
        try:
            data_list = request.data
            my_type = data_list["type"]
            if my_type == "namedict":
                my_team = data_list["team"]
                re_list = []
                re_queryset = User2.objects.all().order_by("username")
                if my_team == "测试中心":
                    re_queryset = re_queryset.filter(team=my_team)
                val_list = re_queryset.values()
                for val in val_list:
                    re_list.append({"username": val["username"], "name": val["name"]})
                my_res["myState"] = "success"
                my_res["myDesc"] = re_list
            elif my_type == "teamdict":
                re_list = []
                re_queryset = User2.objects.only("team")
                val_list = re_queryset.values()
                for val in val_list:
                    if val["team"] not in re_list and val["team"]:
                        re_list.append(val["team"])
                wb_list_do = []
                wb_list_do_keys = []
                wb_list_done = []
                wb_queryset_done = User2.objects.only("username").values()
                for var1 in wb_queryset_done:
                    if var1["username"] not in wb_list_done:
                        wb_list_done.append(var1["username"])
                wb_queryset = tester.objects.all().values()
                for val2 in wb_queryset:
                    if val2["tester_logname"] not in wb_list_done and val2["tester_logname"] not in wb_list_do_keys:
                        wb_list_do.append({"username": val2["tester_logname"], "name": val2["name"]})
                        wb_list_do_keys.append(val2["tester_logname"])
                my_res["myState"] = "success"
                my_res["myDesc"] = {"teamdict": re_list, "wb_list_do": wb_list_do}
            elif my_type == "info":
                re_queryset = list(User2.objects.all().order_by("username").values())
                re_list = []

                wb_list_do_keys = []
                wb_list_done = []
                wb_queryset_done = User2.objects.only("username").values()
                for var1 in wb_queryset_done:
                    if var1["username"] not in wb_list_done:
                        wb_list_done.append(var1["username"])
                wb_queryset = tester.objects.all().values()

                for val2 in wb_queryset:
                    if val2["tester_logname"] not in wb_list_done and val2["tester_logname"] not in wb_list_do_keys:
                        re_list.append({"username": val2["tester_logname"], "name": val2["name"]})
                        wb_list_do_keys.append(val2["tester_logname"])

                for row in re_queryset:
                    row_tmp = {}
                    for key in row:
                        if key in ["name", "username", "level", "team"]:
                            row_tmp[key] = row[key]
                        elif key == "is_active":
                            if row[key]:
                                row_tmp[key] = 1
                            else:
                                row_tmp[key] = 0
                    re_list.append(row_tmp)
                my_res["myState"] = "success"
                my_res["myDesc"] = re_list
            elif my_type == "is_active":
                row = data_list["row"]
                # if row["is_active"] == 1:
                User2.objects.filter(username=row["username"]).filter(name=row["name"]).update(is_active=row["is_active"])
                # elif row["is_active"] == 0:
                #     User2.objects.filter(username=row["username"]).filter(name=row["name"]).update(is_active=1)
                my_res["myState"] = "success"
                my_res["myDesc"] = "状态修改完成"

        except Exception as e:
            my_res["myState"] = "fail"
            my_res["myDesc"] = str(e)
            return HttpResponse(json.dumps(my_res))
        else:
            return HttpResponse(json.dumps(my_res))


# 注册用户
class UserRegViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """用户注册
    """
    serializer_class = UserRegSerializer
    queryset = User2.objects.all()


# 修改密码
class UpdatePasswordView(APIView):
    """修改密码
    """

    def put(self, request):
        """
        根据传的用户名修改密码
        :param request:
        :return:
        """
        data = request.data
        try:
            user = User2.objects.get(username=data['username'])
        except:
            return Response({'message': '账号不存在'})
        if not user.check_password(data['old_password']):
            return Response({'message': '原密码输入有误'})
        if data['password'] != data['password2']:
            return Response({'message': '两次密码不一样,请重新输入'})
        user.set_password(data['password'])
        user.save()
        return Response({'message': 'ok'})
    # def put(self, request, pk):
    #     """
    #     根据传的用户ID修改密码
    #     :param request:
    #     :param pk:
    #     :return:
    #     """
    #     data = request.data
    #     user = User.objects.get(id=pk)
    #     print(user)
    #     if not user.check_password(data['old_password']):
    #         raise Exception('原密码输入有误')
    #     if data['password'] != data['password2']:
    #         raise Exception('两次密码不一样,请重新输入')
    #     user.set_password(data['password'])
    #     user.save()
    #     return Response({'message': 'ok'})


# 重置密码
class ResetPasswordView(APIView):
    """重置密码
    """

    def post(self, request):
        data = request.data
        try:
            user = User2.objects.get(username=data['username'])
        except:
            return Response({"state": "fail", 'message': '账号不存在'})
        # 所有的密码都重置为123456
        newPwd = '%s@1234' % data['username']
        user.set_password(newPwd)
        user.save()
        return Response({"state": "ok", 'message': newPwd})


# class LogoutView(APIView):
#     """退出视图
#     """
#
#     def get(self, request):
#         logout(request)
#         return Response({"message": 'ok'})

# 校验用户名
class UsernameValidateView(APIView):
    """校验用户名"""

    def get(self, request, username):
        data_dict = {
            "username": username,
            "count": User.objects.filter(username=username).count()
        }
        return Response(data_dict)


# 获取角色权限清单
class MyAuthValidateView(APIView):
    """获取角色权限清单"""

    def get(self, request):
        try:
            level = request.GET["level"]
            if level == "all":
                authObj = myauth.objects.all().values()
                authList = {}
                allAuth = []
                auth_level = {}
                for auth in authObj:
                    List = []
                    auths = re.split(",", auth["authlist"])
                    # print(auths)
                    levelVal = auth["level"]
                    for a in auths:
                        if a not in List:
                            List.append(a)
                        if a not in allAuth:
                            allAuth.append(a)
                        if a not in auth_level.keys():
                            auth_level[a] = [levelVal]
                        if a in auth_level.keys():
                            if levelVal not in auth_level[a]:
                                auth_level[a].append(levelVal)
                    authList[levelVal] = List
                authList["allAuth"] = allAuth
                unDict = {}
                for level3 in authList.keys():
                    if level3 != "allAuth":
                        List2 = []
                        for auth2 in authList["allAuth"]:
                            if auth2 not in authList[level3]:
                                if len(List2) == 0:
                                    List2.append(auth2)
                                else:
                                    if auth2 not in List2:
                                        List2.append(auth2)
                        unDict[level3] = List2
                authList["unDict"] = unDict
                authList["auth_level"] = auth_level
            else:
                auth = re.split(",", myauth.objects.filter(level=level).values("authlist")[0]["authlist"])
                authList = []
                for a in auth:
                    if a not in authList:
                        authList.append(a)
        except Exception as e:
            res = "fail"
            desc = str(e)
        else:
            res = "success"
            desc = authList
        return HttpResponse(json.dumps({
            "myState": res,
            "myDesc": desc
        }))

    def post(self, request):
        try:
            dataDict = request.data
            type = dataDict['type']
            if type == "addAuth":
                authDict = dataDict['authList']
                addVal = dataDict['addVal']
                levelList = dataDict['level']
                for key in authDict.keys():
                    if key in levelList:
                        authList = authDict[key]
                        authList.append(addVal)
                        auth = ",".join(itme for itme in authList)
                        authObj = myauth.objects.get(level=key)
                        authObj.authlist = auth
                        authObj.save()
                res = "success"
                desc = authList
            elif type == "delAuth":
                authDict = dataDict['authList']
                delVal = dataDict['delVal']
                for key in authDict.keys():
                    if key not in ("allAuth", "unDict"):
                        authList = authDict[key]
                        if delVal in authList:
                            authList.remove(delVal)
                            auth = ",".join(itme for itme in authList)
                            authObj = myauth.objects.get(level=key)
                            authObj.authlist = auth
                            authObj.save()
                res = "success"
                desc = authList
            elif type == "changeAuth":
                authList = dataDict['authList']
                level = dataDict['level']
                auth = ",".join(itme for itme in authList)
                authObj = myauth.objects.get(level=level)
                authObj.authlist = auth
                authObj.save()
                res = "success"
                desc = authList
            elif type == "auth_level":
                auth_dict = dataDict['authList']
                auth_dict_new = auth_dict
                auth = dataDict['changeVal']
                level_have_new = dataDict['level']
                auth_level = auth_dict["auth_level"]
                # level_have_old = auth_level[auth]
                for level in auth_dict.keys():
                    if level not in ["auth_level", "unDict", "allAuth"]:
                        auth_old = auth_dict[level]
                        if level in level_have_new:
                            if auth not in auth_old:
                                auth_old.append(auth)
                                auth_dict_new[level] = auth_old
                                auth_new = ",".join(itme for itme in auth_old)
                                auth_obj = myauth.objects.get(level=level)
                                auth_obj.authlist = auth_new
                                auth_obj.save()
                        else:
                            if auth in auth_old:
                                auth_new = []
                                for itme in auth_old:
                                    if itme != auth:
                                        auth_new.append(itme)
                                auth_dict_new[level] = auth_new
                                auth_new2 = ",".join(val for val in auth_new)
                                auth_obj = myauth.objects.get(level=level)
                                auth_obj.authlist = auth_new2
                                auth_obj.save()
                res = "success"
                desc = auth_dict_new

        except Exception as e:
            res = "fail"
            desc = str(e)
        return HttpResponse(json.dumps({
            "myState": res,
            "myDesc": desc
        }))
```

## 定义路由

在项目根目录的urls.py中添加

```python
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
# 获取用户名,密码验证通过后返回token
from rest_framework_jwt.views import obtain_jwt_token
# 用户管理
from users.views import UserRegViewSet, UpdatePasswordView, ResetPasswordView, MyAuthValidateView, UserViews

router = routers.DefaultRouter()
# 用户注册
router.register(r'logon', UserRegViewSet, basename='logon')
# 用户信息
router.register(r'userinfo', UserViews, basename='userinfo')

urlpatterns = [
                  
                  url('api/', include(router.urls)),
    			  # 校验密码
                  url(r'^api-token-auth', obtain_jwt_token),
    			  # 登录
                  url(r'^login', obtain_jwt_token),
                  
                  # 根据用户名重置密码
                  path('resetpwd/', ResetPasswordView.as_view()),
                  # 修改密码
                  path('updatepwd/', UpdatePasswordView.as_view()),
                  path('myauth/', MyAuthValidateView.as_view()),
                  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                 
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Django管理端注册用户

- 创建超级管理员，后登录超级管理员，进入以下页面，可以看见注册页面

  ```
  http://127.0.0.1:8000/api/users
  ```

- 修改users模块下的admin.py，使用户模块可以在管理端展示及修改

  ```python
  from django.contrib import admin
  
  # Register your models here.
  from .models import UserProfile
  class UserAdmin(admin.ModelAdmin):
      list_display=["name","username","usernum","last_login","level","date_joined"]
  
  admin.site.register(UserProfile,UserAdmin)
  ```

# 创建项目组件（功能）

## 创建组件

```python
python manage.py startapp HuanJingGuanLi(组件名称)
```

## 配置组件功能

通过数据库模板，在数据库内创建表

- 修改HuanJingGuanLi文件内的models.py

  ```python
  from django.db import models
  
  # Create your models here.
  class huanjing(models.Model):
      sys=models.CharField(max_length=200) 
      SIT1=models.CharField(max_length=200)
      SIT2 = models.CharField(max_length=200)
      SIT3 = models.CharField(max_length=200)
      SIT4 = models.CharField(max_length=200)
      remarks= models.CharField(max_length=200)
  ```

- 在项目根目录的setting.py内增加'HuanJingGuanLi.apps.HuanjingguanliConfig'

  ```python
  INSTALLED_APPS = [
      'HuanJingGuanLi.apps.HuanjingguanliConfig',
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
  ]
  
  ps：'HuanJingGuanLi.apps.HuanjingguanliConfig'
  HuanJingGuanLi：组件名称
  apps：HuanJingGuanLi内的apps方法
  HuanjingguanliConfig：apps方法内的类名
  ```

## 将功能数据写入数据库（创建表）

```python
python manage.py makemigrations
python manage.py migrate
```

## 将功能引入后台管理

修改HuanJingGuanLi目录下的admin.py

```python
from django.contrib import admin

# Register your models here.
from .models import huanjing
class HanjingAdmin(admin.ModelAdmin):
    list_display=["sys","SIT1","SIT2","SIT3","SIT4","remarks"]

admin.site.register(huanjing,HanjingAdmin)
```

# 创建存放网页模板的文件夹templates

```
目录：D:\TCweb下
修改settings.py内的TEMPLATES， 'DIRS'的值改为 [os.path.join(BASE_DIR,'templates')
```

# 模板的加载方式

方案1	通过loader获取模板s

```
from django.template import loader
#1.通过loader加载模板
t = loader.get_template("模板文件名")
#2.将t转换成HTML字符串
html=t.render（字典数据）
#3.用响应对象浙江转换的字符串内容返回给浏览器
return HttpResponse(html)
```

方案2	使用render()直接加载并响应模板

```
在视图函数中：
from django.shortcuts import render
return render(request,'模板文件名',字典数据)
```

# 创建视图文件views.py

```
目录：D:\TCweb\TCweb下
文件内编辑：
from  django.http import HttpResponse
自定义视图函数
def log_view(request):
    return render(request,'login.html')
```

# 配置主路由

```
 urlpatterns中添加
 path('', views.log_view)
```

# 对外提供服务

```
#允许使用本机IP访问
ALLOWED_HOSTS = ['127.0.0.1','10.16.87.246']
cd D:\TCweb
#启动项目
python manage.py runserver 0.0.0.0:8000
#局域网访问
http://10.16.87.246:8000/
```

# oracle查询

新建文件夹templates，进入templates新建page.html，写入

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>早上好</title>
    </head>
    <body>
        <h1>{{tmp}}</h1>
        <h2>{{tmp2}}</h2>
    </body>
</html>
```

新建一个views.py，写入

```Python
from django.http import HttpResponse 
from django.urls import path 
from django.shortcuts import render 
import cx_Oracle

#设置环境变量
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK'
os.environ['ORACLE_HOME'] = r'instantclient 的系统路径'
os.environ['path'] = r'instantclient 的系统路径'

conn = cx_Oracle.connect('账户/密码@IP:端口号/数据库实例名',encoding="UTF-8") 
cursor = conn.cursor() 
def hello(request):
    return HttpResponse("Hello world ! ") 
def pen(request):
    my_list=['apple','banana','orange']  #return render(request,"page.html",{"tmp":my_list})
    sql = "查询语句"
    cursor.execute(sql)
    row = cursor.fetchall()
    yiru=[]
    for i in range(len(row)):
        yiru.append(row[i][0])
        return render(request,"page.html",{"tmp":my_list,"tmp2":yiru}) 
```

修改urls.py

```python
from django.conf.urls import url
from . import views
from django.urls import path
urlpatterns = [ path('a_name/',views.pen), ]
```

修改settings.py，将TEMPLATES下的'DIRS': []改成

```
'DIRS': [os.path.join(BASE_DIR, 'templates')],
```

# 问题记录

- 登录验密报错：

  ```
  File "/root/anaconda3/lib/python3.11/site-packages/djangorestframework_jwt-1.11.0-py3.11.egg/rest_framework_jwt/utils.py", line 96, in jwt_encode_handler
      ).decode('utf-8')
        ^^^^^^
  AttributeError: 'str' object has no attribute 'decode'
  ```

  问题分析：

  使用的PyJWT版本较高，卸载后安装PyJWT-1.7.1，解决
  
- 修改密码报错：

  ```
  Internal Server Error: /updatepwd/
  Traceback (most recent call last):
   .....
  AssertionError: Cannot apply DjangoModelPermissionsOrAnonReadOnly on a view that does not set `.queryset` or have a `.get_queryset()` method.
  ```

  解决方案：

  /settings.py中注释以下内容

  ```
  # REST_FRAMEWORK = {
  #     'DEFAULT_PERMISSION_CLASSES': [
  #         'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
  #     ]
  # }
  ```

  



