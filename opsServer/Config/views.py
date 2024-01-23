from django.shortcuts import render
from .models import menu, WebAuth, UserAuth
from rest_framework import viewsets, mixins
from .serializers import WebMenuSerializer
from django.db import connection
from django.http import HttpResponse
import json
# Create your views here.


class WebMenuViews(viewsets.ModelViewSet):
    serializer_class = WebMenuSerializer

    # fields = ["cust_num", "cust_name", "cust_sex", "label", "remarks"]
    # def __init__(self, **kwargs):
    #     super().__init__(kwargs)
    #     self.re_list = []

    def get_queryset(self):
        return WebMenu.objects.filter(state=1)

    def create(self, request, *args, **kwargs):
        my_res = {"myState": "success", "myDesc": ""}
        try:
            data_list = request.data
            my_type = data_list["type"]
            if my_type == "getMenu":
                my_role = data_list["role"]
                # 权限 id清单
                auth_list = []
                # role 权限id清单
                role_list = list(WebAuth.objects.filter(state=1).filter(role=my_role).filter(switch=1).values_list("mid"))
                for row in role_list:
                    auth_list.append(row[0])
                if "username" in data_list.keys():
                    m_user = data_list["username"]
                    # 用户 权限id清单
                    user_list = list(UserAuth.objects.filter(state=1).filter(switch=1).filter(username=m_user).values_list("mid"))
                    for row in user_list:
                        if row[0] not in auth_list:
                            auth_list.append(row[0])
                # 最后返回的menu清单
                my_list = []
                menu_list = []
                # 获取符合条件的全部queryset
                self.queryset = menu.objects.filter(state=1).filter(id__in=auth_list)
                # 获取首层菜单清单
                top_level_list =list(self.queryset.filter(fid=0).order_by("index").values())
                for row in top_level_list:
                    top_level = self.get_dict(row)
                    my_list.append(top_level)
                my_res["myState"] = "success"
                my_res["list"] = my_list
                # my_res["menu"] = menu_list
            elif my_type == "getAuth":
                if "role" in data_list.keys():
                    my_role = data_list["role"]
                    # 获取已经具有权限的功能mid清单，values_list返回的是一个元祖组成的list：[(2,), (1,)]
                    yes_rows = list(WebAuth.objects.filter(state=1).filter(switch=1).filter(role=my_role).values_list("mid"))
                elif "username" in data_list.keys():
                    m_user = data_list["username"]
                    yes_rows = list(UserAuth.objects.filter(state=1).filter(switch=1).filter(username=m_user).values_list("mid"))

                yes_id_list = []
                for row in yes_rows:
                    yes_id_list.append(row[0])
                # 获取已经拥有权限的功能清单
                yes_list = list(menu.objects.filter(id__in=yes_id_list).filter(has_child=0).values()) 
                # 获取不具备权限的功能清单
                no_list = list(menu.objects.filter(state=1).filter(has_child=0).exclude(id__in=yes_id_list).values())

                my_res["myState"] = "success"
                my_res["yes_list"] = yes_list
                my_res["no_list"] = no_list
            elif my_type == "changeAuth":
                auth_list = data_list["authList"]
                # 按角色修改权限
                if "role" in data_list.keys():
                    role = data_list['role']
                    # 修改角色对应的状态
                    WebAuth.objects.filter(role=role).update(state=False)
                    for mid in auth_list:
                        while True:
                            the_menu = menu.objects.get(id=mid)
                            m_path = the_menu.path
                            # 根据path的值，更新menu权限中已经的项的mid的值
                            auth_one = WebAuth.objects.filter(m_path=m_path).filter(role=role)
                            if auth_one:
                                auth_one.update(mid=mid,state=True,switch=True)
                            else:
                                WebAuth.objects.create(mid=mid,m_path=m_path,role=role,switch=True,state=True)
                            if the_menu.fid > 0:
                                mid = the_menu.fid
                            else:
                                break

                elif "username" in data_list.keys():
                    username = data_list['username']
                    UserAuth.objects.filter(username=username).update(state=False)
                    for mid in auth_list:
                        while True:
                            the_menu = menu.objects.get(id=mid)
                            m_path = the_menu.path
                            # 根据path的值，更新menu权限中已经的项的mid的值
                            auth_one = UserAuth.objects.filter(m_path=m_path).filter(username=username)
                            if auth_one:
                                auth_one.update(mid=mid,state=True,switch=True)
                            else:
                                UserAuth.objects.create(mid=mid,m_path=m_path,username=username,switch=True,state=True)
                            if the_menu.fid > 0:
                                mid = the_menu.fid
                            else:
                                break
                
            # elif my_type == "openAuth":
            #     name = data_list["name"]
            #     levels = data_list["levels"]
            #     if "," in levels:
            #         level_list = re.split(",", levels)
            #     else:
            #         level_list = [levels]
            #     for level in level_list:
            #         WebAuth.objects.filter(level=level).filter(name=name).update(switch=1)
            elif my_type == "updateMenu":
                my_value = data_list["value"]
                val_json = json.loads(my_value)
                the_list = val_json["data"]["list"]
                # print(val_json["data"]["list"])
                # 清空数据库中的内容
                menu.objects.all().delete()
                # 获取数据库表名
                table_name = menu._meta.db_table
                # 重置表id
                with connection.cursor() as cursor:
                    cursor.execute(f"ALTER TABLE {table_name} AUTO_INCREMENT = 1;")
                # 将权限（角色）列表状态置为0
                WebAuth.objects.all().update(state=0)
                # 将权限（用户）列表状态置为0
                UserAuth.objects.all().update(state=0)
                # 获取menu数据，并写入到数据库
                for index,dict_var in enumerate(the_list,start=1):
                    fid = 0
                    step = 1
                    # up_level = dict_var["meta"]["title"]
                    self.getvar(dict_var, index, fid, step)                
                
                
        except Exception as e:
            my_res["myState"] = "fail"
            print(f"updateMenu,err,{e}")
            my_res["myDesc"] = str(e)
            return HttpResponse(json.dumps(my_res))
        else:
            return HttpResponse(json.dumps(my_res))

    def write_db(self,data_dict):
        """将数据写入数据库"""
        # 将menu数据写入数据库
        new_one = menu()
        new_one.path = data_dict["path"]
        new_one.redirect = data_dict["redirect"]
        new_one.meta_title = data_dict["meta_title"]
        new_one.meta_icon = data_dict["meta_icon"]
        new_one.meta_cache = data_dict["meta_cache"]
        new_one.alway_show = data_dict["alway_show"]
        new_one.hideClose = data_dict["hideClose"]
        new_one.component = data_dict["component"]
        new_one.fid = data_dict["fid"]
        new_one.step = data_dict["step"]
        new_one.index = data_dict["index"]
        new_one.has_child = data_dict["has_child"]
        new_one.state = data_dict["state"]
        new_one.save()
        # 根据path的值，更新menu权限（角色）中已经的项的mid的值
        auth_one = WebAuth.objects.filter(m_path=data_dict["path"])
        if auth_one:
            auth_one.update(mid=new_one.id,state=True)
        else:
            WebAuth.objects.create(mid=new_one.id,m_path=data_dict["path"],role="SuperAdmin",switch=True,state=True)
        # 根据path的值，更新menu权限（用户）中已经的项的mid的值
        auth_one = UserAuth.objects.filter(m_path=data_dict["path"])
        if auth_one:
            auth_one.update(mid=new_one.id,state=True)
        # else:
        #     UserAuth.objects.create(mid=new_one.id,m_path=data_dict["path"],role="SuperAdmin",switch=True,state=True)
      
    def getvar(self, v, index, fid, step):
        if "children" in v.keys():
            self.add_var(v, index, fid, step,has_child=True)
            up_id = menu.objects.get(path=v["path"]).id
            step += 1
            for i,v1 in enumerate(v["children"],start=1):
                self.getvar(v1, i,up_id,step)
        else:
            self.add_var( v, index, fid, step,has_child=False)

    def add_var(self,  v, index, fid, step,has_child):
        if "redirect" in v.keys():
            redirect = v["redirect"]
        else:
            redirect = ""
        if "icon" in v["meta"].keys():
            icon = v["meta"]["icon"]
        else:
            icon = ""
        if "hideClose" in v.keys():
            hide_close = v["hideClose"]
        else:
            hide_close = ""
        if "component" in v.keys():
            component = v["component"]
        else:
            component = ""
        if "alwayShow" in v.keys():
            alway_show = v["alwayShow"]
        else:
            alway_show = ""
        if "cache" in v.keys():
            meta_cache = v["cache"]
        else:
            meta_cache = ""
        re_list = { "path": v["path"],"redirect": redirect, "meta_title": v["meta"]["title"], "meta_icon": icon, "meta_cache": meta_cache,"alway_show": alway_show, "hideClose": hide_close, "component": component, "fid": fid, "step": step,"index":index,"has_child":has_child,"state": 1}
        self.write_db(re_list)

    def get_children(self, row):
        re_list = []
        fid = row["id"]
        children_list = list(self.queryset.filter(fid=fid).order_by("index").values())
        for r in children_list:
            re_list.append(self.get_dict(r))

        return re_list

    def get_dict(self, row):
        my_dict = {"path": row["path"]}
        if row["redirect"]:
            my_dict["redirect"] = row["redirect"]
        if row["alway_show"]:
            my_dict["alwayShow"] = row["alway_show"]
        meta = {"title": row["meta_title"]}
        if row["meta_icon"]:
            meta["icon"] = row["meta_icon"]
        if row["hideClose"]:
            meta["hideClose"] = True
        if row["meta_cache"]:
            meta["cache"] = True
        my_dict["meta"] = meta
        if row["component"]:
            my_dict["component"] = row["component"]
        if row["has_child"]:
            my_dict["children"] = self.get_children(row)
        return my_dict

