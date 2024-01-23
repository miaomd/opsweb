from django.shortcuts import render
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegSerializer, UserInfoSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
# from .models import myauth
# from ZiYuanChi.models import tester
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
            if my_type == "roleList":
                re_list = list(User2.objects.values_list("role",flat=True).distinct())
                my_res["myState"] = "success"
                my_res["myDesc"] = re_list
            elif my_type == "userList":
                re_list = list(User2.objects.filter(is_active=1).values_list("username","name"))
                my_res["myState"] = "success"
                my_res["myDesc"] = re_list
            elif my_type == "info":
                re_queryset = list(User2.objects.all().order_by("username").values())
                re_list = []
                for row in re_queryset:
                    row_tmp = {}
                    for key in row:
                        if key in ["name", "username", "role"]:
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
            queryset = list(User2.objects.all().values())
            user_name = data['username']
            user = User2.objects.get(username=user_name)
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
