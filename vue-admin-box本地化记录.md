# 网站基本信息信息修改

## 修改网站名和登录页信息

- 路径：\src\locale\modules\zh-cn\system.ts

## 修改网站图标

- 路径：index.html

- 新图标放到 public 下

- 修改图标地址

  ```html
  <link rel="icon" href="/TrcBank.ico" />
  ```

## logo顶部模块和历史导航页签

- 路径:src\store\modules\app.ts

- 修改默认值

  ```javascript
  const state = () => ({
    showLogo: false, // 是否显示Logo
    showTabs: false, // 是否显示导航历史
  })
  ```

## 隐藏自带页面

\src\router\permission\front.ts

```javascript
/**
 * 前端路由管理
 **/

/** 路由类型 */
import type { Route } from '../index.type'

/** 引入需要权限的Modules */
import Dashboard from '../modules/dashboard'
import Document from '../modules/document'
import Pages from '../modules/pages'
import Menu from '../modules/menu'
import Component from '../modules/component'
import Directive from '../modules/directive'
import SystemManage from '../modules/systemManage'
import Chart from '../modules/chart'
import Print from '../modules/print'
import Community from '../modules/community'
import Tab from '../modules/tab'

/** 登录后需要动态加入的本地路由 */
const FrontRoutes: Route[] = [
  // ...Dashboard,
  // ...Document,
  // ...Component,
  // ...Pages,
  // ...Menu,
  // ...Directive,
  // ...Chart,
  // ...SystemManage,
  // ...Print,
  // ...Community,
  // ...Tab,
]

export default FrontRoutes
```



## 修改BASE_URL

- 开发环境

  ```
  .env.development
  ```

- 生产环境

  ```
  .env.production
  ```

- 测试环境

  ```
  .env.staging
  ```

## 修改元素获取方式

- public\font，新建文件夹存放所需元素

- index.html

  ```
  <link rel="stylesheet" href="//at.alicdn.com/t/font_2570680_gkyjimtz1d.css">
  替换成
  <link rel="stylesheet" href="/font/font_2570680_gkyjimtz1d.css">
  ```

## 修改端口号

- 路径：vite.config.ts

- 参数说明

  ```javascript
      server: {
        // 端口号
        port: 8080,
        // ip
        host: '0.0.0.0',
        // 运行时打开网页
        open: true,
        // 代理
        proxy: { // 代理配置
          '/dev': 'https://www.fastmock.site/mock/48cab8545e64d93ff9ba66a87ad04f6b/'
        },
      },
  ```

  

## 重写统一的应答处理

- 路径：src\utils\system\request.ts

- 重写为：

  ```javascript
  service.interceptors.response.use(
    (response: AxiosResponse) => {
      // const res = response.data
      if ([200, 201].includes(response.status)) {
        return response
      } else {
        showError(response)
        return Promise.reject(response)
      }
    },
    (error: AxiosError)=> {
      console.log(error) // for debug
      const badMessage: any = error.message || error
      const code = parseInt(badMessage.toString().replace('Error: Request failed with status code ', ''))
      showError({ code, message: badMessage })
      return Promise.reject(error)
    }
  )
  ```

# 修改登录api

## 修改登录页上传字段

- 路径：src\views\system\login.vue

- 根据后端接口，修改上传的字段名 username 和 password

  ```javascript
      const submit = () => {
        checkForm()
        .then(() => {
          form.loading = true
          let params = {
            username: form.name,
            password: form.password
          }
          store.dispatch('user/login', params)
          .then(async () => {
            ElMessage.success({
              message: '登录成功',
              type: 'success',
              showClose: true,
              duration: 1000
            })
            location.reload()
            // await getAuthRoutes()
            // await router.push(route.query.redirect as RouteLocationRaw || '/')
          }).finally(() => {
            form.loading = false
          })
        })
      }
  
  ```

## 修改store 中定义的调用登录和获取客户信息api并存储信息的方法

- 路径：src\store\modules\user.ts

- 登录并存储到 store 中

  ```javascript
  const actions = {
    // login by login.vue
    login({ commit, dispatch }: ActionContext<userState, userState>, params: any) {
      return new Promise((resolve, reject) => {
        // 登录的api
        loginApi(params)
        .then(res => {
          // 获取登录后返回的token，调用store中的tokenChange方法将token存到到store中
          commit('tokenChange', res.data.token)
          // 调用下面的 getInfo 方法，获取用户信息
          dispatch('getInfo', { token: res.data.token })
          .then(infoRes => {
            resolve(res.data.token)
          })
        }).catch(err => {
          reject(err)
        })
      })
    },
    // get user info after user logined
    getInfo({ commit }: ActionContext<userState, userState>, params: any) {
      return new Promise((resolve, reject) => {
        //调用用户信息查询接口，查询用户信息
        getInfoApi(params)
        .then(res => {
          // 调用store 中的infoChange 方法，存储用户信息
          commit('infoChange', res.data.info)
          resolve(res.data.info)
        })
      })
    },
  
    // login out the system after user click the loginOut button
    loginOut({ commit }: ActionContext<userState, userState>) {
      loginOutApi()
      .then(res => {
  
      })
      .catch(error => {
  
      })
      .finally(() => {
        localStorage.removeItem('tabs')
        localStorage.removeItem('vuex')
        sessionStorage.removeItem('vuex')
        location.reload()
      })
    }
  }
  ```

## 修改登录api

- 路径：src\api\user.ts

- 登录和获取用户信息的api

  ```javascript
  /** 登录api */
  export function loginApi(data: object) {
    return request({
      url: '/login',
      method: 'post',
      // baseURL: '/mock',
      data
    })
  }
  
  /** 获取用户信息Api */
  export function getInfoApi(data: object) {
    return request({
      url: '/user/info',
      method: 'post',
      baseURL: '/mock',
      data
    })
  }
  
  ```

# 头部组件自定义

- 路径：src\layout\Header\index.vue
- 不需要的组件直接注释掉

## 用户信息动态获取

- script 中从 store实时获取用户信息

  ```javascript
  <script lang="ts">
  import { useStore } from 'vuex'
  export default defineComponent({
        setup() {
                const store = useStore()
                // 读取store中的用户信息
                const userInfo = computed(() => store.state.user.info).value
        }
         return {
      	userInfo,
  	  }                               
  })
  ```

- template 中 将用户信息字段替换成

  ```html
            <span class="el-dropdown-link">
              {{userInfo.name }}
              <i class="sfont system-xiala"></i>
            </span>
  ```

## 修改密码优化

- src\layout\Header\passwordLayer.vue

- 修改密码时录入两遍新密码，且增加新密码复杂度规则

  ```
  <template>
    <Layer :layer="layer" @confirm="submit" ref="layerDom">
      <el-form :model="form" :rules="rules" ref="ruleForm" label-width="120px" style="margin-right:30px;">
        <el-form-item label="登录名：" prop="name">
          {{ form.username }}
        </el-form-item>
        <el-form-item label="原密码：" prop="old_password">
          <el-input v-model="form.old_password" placeholder="请输入原密码" show-password></el-input>
        </el-form-item>
        <el-form-item label="新密码：" prop="password">
          <el-input v-model="form.password" placeholder="请输入新密码" show-password></el-input>
        </el-form-item>
        <el-form-item label="再一次：" prop="password2">
          <el-input v-model="form.password2" placeholder="再一次新密码" show-password></el-input>
        </el-form-item>
  
      </el-form>
    </Layer>
  </template>
  
  <script lang="ts">
  import type { LayerType } from '@/components/layer/index.vue'
  import type { Ref } from 'vue'
  import type { ElFormItemContext } from 'element-plus/lib/el-form/src/token'
  import { defineComponent, ref, computed } from 'vue'
  import { ElMessage } from 'element-plus'
  import { useStore } from 'vuex'
  import { passwordChange } from '@/api/user'
  import Layer from '@/components/layer/index.vue'
  export default defineComponent({
    components: {
      Layer
    },
    props: {
      layer: {
        type: Object,
        default: () => {
          return {
            show: false,
            title: '',
            showButton: true
          }
        }
      }
    },
    setup(props, ctx) {
      const ruleForm: Ref<ElFormItemContext | null> = ref(null)
      const layerDom: Ref<LayerType | null> = ref(null)
      const store = useStore()
      const userInfo = computed(() => store.state.user.info).value
  
      let form = ref({
        Name: "",
        Level: "",
        username: userInfo.username,
        old_password: "",
        password: "",
        password2: "",
      })
      const rules = {
        old_password: [{ required: true, message: '请输入原密码', trigger: 'blur' }
        ],
        password: [{ required: true, message: '请输入新密码', trigger: 'blur' },
        { pattern: /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,16}$/, message: '密码为8~16位且同时包含,数字+大小写字母+特殊符号', trigger: 'blur' }],
        password2: [{ required: true, message: '再一次新密码', trigger: 'blur' },
        { pattern: /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,16}$/, message: '密码为8~16位且同时包含,数字+大小写字母+特殊符号', trigger: 'blur' }],
  
      }
      function submit() {
        if (ruleForm.value) {
          ruleForm.value.validate((valid) => {
            if (valid) {
              // let params = {
              //   id: form.value.userId,
              //   old: form.value.old,
              //   new: form.value.new
              // }
              console.log("form", form)
              passwordChange(form.value)
                .then(res => {
                  let changeRe = res.data;
                  if (changeRe.message == "ok") {
                    ElMessage({
                      type: 'success',
                      message: '密码修改成功，即将跳转到登录页面'
                    })
                    layerDom.value && layerDom.value.close()
                    setTimeout(() => {
                      store.dispatch('user/loginOut')
                    }, 2000)
                  } else {
                    // alert(changeRe.message);
  
                    ElMessage({
                      message: changeRe.message,
                      type: "error",
                    });
                  }
                })
            } else {
              return false;
            }
          });
        }
      }
      return {
        form,
        rules,
        layerDom,
        ruleForm,
        submit
      }
    }
  })
  </script>
  
  <style lang="scss" scoped></style>
  ```

  



# 使用后端路由控制菜单展示

## 后端创建数据库表

- Django创建Config模块

  ```
  python manage.py startapp Config
  ```

- 通过数据库模板，在数据库内创建表

  修改Config文件内的models.py

  ```python
  from django.db import models
  
  # Create your models here.
  
  class menu(models.Model):
      """前端的导航菜单"""
      path = models.CharField(max_length=100, null=False, blank=True, verbose_name="路径")
      redirect = models.CharField(max_length=100, null=False, blank=True, verbose_name="重定向")
      meta_title = models.CharField(max_length=50, null=False, blank=True, verbose_name="路由名")
      meta_icon = models.CharField(max_length=50, null=False, blank=True, verbose_name="图标")
      meta_cache = models.CharField(max_length=50, null=False, blank=True, verbose_name="cache")
      alway_show = models.CharField(max_length=50, null=False, blank=True, verbose_name="alwayShow")
      hideClose = models.CharField(max_length=50, null=False, blank=True, verbose_name="是否隐藏")
      component = models.CharField(max_length=100, null=False, blank=True, verbose_name="component")
      fid = models.IntegerField( null=False, blank=True,default=0, verbose_name="上级id")
      step = models.IntegerField(null=True, blank=True, verbose_name="层级深度")
      index = models.IntegerField(null=True, blank=True, verbose_name="层级内顺序号")
      has_child = models.BooleanField(null=False, blank=False,default=False, verbose_name="是否有下级")
      state  = models.BooleanField(null=False, blank=False,default=False, verbose_name="状态")
  
  class WebAuth(models.Model):
      """权限-角色"""
      mid =  models.IntegerField( null=False, blank=True, verbose_name="菜单id")
      m_path = models.CharField(max_length=100, null=False, blank=True, verbose_name="menu路径")
      role = models.CharField(max_length=50, null=False, blank=True, verbose_name="角色")
      switch = models.BooleanField(null=False, blank=False,default=False, verbose_name="开关")
      state = models.BooleanField(null=False, blank=False,default=False, verbose_name="状态")
  
  class UserAuth(models.Model):
      """权限-用户"""
      mid =  models.IntegerField( null=False, blank=True, verbose_name="菜单id")
      m_path = models.CharField(max_length=100, null=False, blank=True, verbose_name="menu路径")
      username = models.CharField(max_length=50, null=False, blank=True, verbose_name="用户登录名")
      switch = models.BooleanField(null=False, blank=False,default=False, verbose_name="开关")
      state = models.BooleanField(null=False, blank=False,default=False, verbose_name="状态")
  ```

- 在项目根目录的setting.py内增加'Config'

  ```python
   INSTALLED_APPS = [
        'Config',
    ]
  ```

- 将功能数据写入数据库（创建表）

  ```
  python manage.py makemigrations Config
  python manage.py migrate
  ```

## 前端编辑menu

- 路径：src\views\main\systemManage\menu\index.vue

- 增加：

  ```js
  <template>
    <div class="layout-container">
      <div class="layout-container-table">
        <div ref="dom" />
        <el-card class="box-card">
          <template #header>
            <p style="text-align: left;">
              v-model结果
              <el-button style="float: right; padding: 3px 0" type="text" @click="updateData"
                v-if="codeDataOld != codeData">更新菜单</el-button>
  
              <el-button style="float: right; padding: 3px 0" type="text" @click="setData">初始赋值</el-button>
  
            </p>
          </template>
          <pre>{{ codeData }}</pre>
        </el-card>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted, watch } from 'vue'
  // load basic codemirror
  import codeMirror, { CodeMirror } from 'codemirror'
  import 'codemirror/lib/codemirror.css'
  // load model
  import 'codemirror/mode/javascript/javascript'
  // load codetip
  import 'codemirror/addon/lint/lint'
  import 'codemirror/addon/lint/json-lint'
  import 'codemirror/theme/3024-night.css'
  import { getMenuApi, updateMenuApi } from '@/api/user'
  
  export default defineComponent({
    setup() {
      let dom = ref(null)
      let codeData = ref('')
      let codeDataOld = ref('')
      let editor: any = ref(null)
      let timer = null
      let editorChange = false
      const options = {
        value: codeData.value,
        lineNumbers: true,
        mode: 'application/json',
        theme: '3024-night'
      }
      onMounted(() => {
        editor = codeMirror(dom.value, options)
        handleChange()
      })
      function handleChange() {
        editor.on('changes', (instance: CodeMirror, changes: Array<object>) => {
          editorChange = true
          timer = null
          codeData.value = editor.getValue()
          timer = setTimeout(() => {
            editorChange = false
          }, 50)
        })
      }
      // watch the codeData change but not from editor change
      watch(codeData, (newVal, oldVal) => {
        if (!editorChange) {
          setEditorData()
        }
      })
      function updateData() {
        let params = { type: "updateMenu", value: codeData.value };
        updateMenuApi(params).then((res) => {
          setData()
        })
      }
      // to show how to do a v-model demo
      function setData() {
        codeData.value = ""
        codeDataOld.value = ""
  
        let params = { type: "getMenu", role: "SuperAdmin" };
  
        getMenuApi(params).then((res) => {
          // console.log(res.data.list)
          codeDataOld.value = JSON.stringify({
            code: 200,
            msg: '请求成功',
            data: {
              list: res.data.list
            }
          }, null, 2)
          codeData.value = codeDataOld.value
        })
      }
      // set editor data anytime when you use this function
      function setEditorData() {
        editor.getDoc().setValue(codeData.value)
      }
      return {
        dom,
        codeData,
        codeDataOld,
        setData,
        updateData
      }
    }
  })
  </script>
  
  <style lang="scss" scoped>
  * {
    text-align: left;
  }
  
  #codeEditor {
    text-align: left;
  }
  
  pre {
    text-align: left;
  }
  </style>
  ```

- 使用json格式管理menu

  ```json
  {
    "code": 200,
    "msg": "请求成功",
    "data": {
      "list": [
        {
          "path": "/",
          "redirect": "/dashboard",
          "meta": {
            "title": "dashboard",
            "icon": "sfont system-home"
          },
          "children": [
            {
              "path": "dashboard",
              "redirect": "/env",
              "meta": {
                "title": "首页",
                "icon": "sfont system-home"
              },
              "component": "dashboard_dashboard"
            }
          ]
        },
        {
          "path": "/systemManage",
          "redirect": "/systemManage/menu",
          "alwayShow": "True",
          "meta": {
            "title": "系统管理",
            "icon": "sfont system-shezhi"
          },
          "children": [
            {
              "path": "menu",
              "meta": {
                "title": "菜单"
              },
              "component": "systemManage_menu"
            },
            {
              "path": "auth",
              "meta": {
                "title": "权限管理"
              },
              "children": [
                {
                  "path": "auth-role",
                  "meta": {
                    "title": "按角色管理"
                  },
                  "component": "systemManage_authrole"
                },
                {
                  "path": "auth-user",
                  "meta": {
                    "title": "按用户管理"
                  },
                  "component": "systemManage_authuser"
                }
              ]
            },
            {
              "path": "user",
              "meta": {
                "title": "用户管理"
              },
              "component": "systemManage_user"
            }
          ]
        }
      ]
    }
  }
  ```

## 后端处理menu变更

```python
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


```

## 前端配置后端路由

- 路径：src\router\permission\backConfig.ts
- menu中**component**字段，通过  **_**  分隔，获取键值
- component，中除了用于分隔   _   不要使用   _

## 修改api请求地址

- 路径：src\api\user.ts

- 修改：

  ```javascript
  /** 获取登录后需要展示的菜单 */
  export function getMenuApi(data: object) {
    return request({
      url: '/api/webmenu/',
      method: 'post',
      // baseURL: '/mock'
      data
    })
  }
  ```

## 后端路由开关

- 路径：src\config\index.ts

- 修改内容

  ```javascript
  /** 使用后端路由 */
  const isBackMenu = true
  ```

## 修改 getMenu 

- 路径：src\router\permission\back.ts

- 修改

  ```javascript
  import store from '@/store'
  
  /** 获取后台模板配置清单 */
  const getMenu = async () => {
    let params = { type: "getMenu", role: store.state.user.info.role, username: store.state.user.info.username };
    const result = await getMenuApi(params)
    const backRoutes = getComponents(result.data.list)
    return backRoutes
  }
  ```
  
  ps:在 .ts 文件中引入 store 不能  import { useStore } from 'vuex'

# 增加系统管理模块

## 新建页面

- 用户管理

  src\views\main\systemManage\users

- 导航栏管理

  src\views\main\systemManage\menu

- 权限管理

  src\views\main\systemManage\role

## 创建路由

src\router\modules\systemManage.ts

## 添加到前端路由

- src\router\permission\front.ts

  ```
  import SystemManage from '../modules/systemManage'
  const FrontRoutes: Route[] = [
    ...SystemManage,
  ]
  ```

  

# 创建新的页面

## 新建页面

- 路径：src\views\main

## 创建路由文件

- 路径：src\router\modules

- title 可以写死，如果从 message中读取，需要修改

  ```
  src\locale\modules\zh-cn\menu.ts
  ```

- 路径：src\router\permission\backConfig.ts

  - 增加页面信息
  - 添加到 allRoutes

## 后端路由中添加显示

- 数据库中增加

# 生产环境部署

使用NGINX 部署vue 项目

## 构建Vue项目

- 在本地使用Vue CLI等工具构建你的Vue项目。执行如下命令：

  ```
  npm run build
  ```

  这将在你的项目目录下生成一个dist文件夹，包含了构建好的静态文件。


## 安装NGINX

- 如果还未安装NGINX，首先需要在服务器上安装NGINX。使用适合你操作系统的包管理器，例如在Ubuntu上使用apt：

  ```
  sudo apt update
  sudo apt install nginx
  ```

##  启动 Nginx：

```
sudo systemctl start nginx
```

手动安装编译，采用一下方式

/usr/local/nginx/sbin/

```
cd /data/nginx/sbin
./nginx
```

或者

```
/data/nginx/sbin/nginx
```

nginx关闭

```
ps –ef | grep nginx 列出Nginx的相关进程
kill pid 杀死Nginx相关进程，也相当于停止Nginx
```

或者

```
/data/nginx/sbin/nginx -s stop 停止Nginx
```

## 设置开机启动：

```
sudo systemctl enable nginx
```

### 如果手动编译和安装 Nginx：

如果你手动编译和安装了 Nginx，你可能需要创建一个 systemd 服务单元文件。

1. **在 `/etc/systemd/system/` 目录中创建 `nginx.service` 文件：**

   ```
   sudo nano /etc/systemd/system/nginx.service
   ```

   将以下内容粘贴到文件中：

   ```
   [Unit]
   Description=nginx - high performance web server
   After=network.target
   
   [Service]
   ExecStart=/usr/local/nginx/sbin/nginx
   ExecReload=/usr/local/nginx/sbin/nginx -s reload
   ExecStop=/usr/local/nginx/sbin/nginx -s stop
   KillMode=process
   Restart=on-failure
   RestartSec=3
   PrivateTmp=true
   
   [Install]
   WantedBy=multi-user.target
   ```

   注意：确保 `ExecStart`、`ExecReload` 和 `ExecStop` 的路径正确，根据你的安装路径进行调整。

2. **重新加载 systemd 配置：**

   ```
   sudo systemctl daemon-reload
   ```

3. **启动 Nginx 服务：**

   ```
   sudo systemctl start nginx
   ```

   

## 配置NGINX

- 查看Nginx配置文件的位置

  ```
  sudo find / -name nginx.conf
  ```

- 打开NGINX配置文件，通常在/etc/nginx/nginx.conf或/etc/nginx/sites-available/default，使用文本编辑器进行编辑：

  ```
  sudo nano /etc/nginx/nginx.conf
  ```

  或

  ```
  sudo nano /etc/nginx/sites-available/default
  ```

- 在配置文件中添加一个新的server块，配置NGINX以服务你的Vue.js项目：

  ```
  server {
      listen 80;
      server_name your_domain.com; # 替换为你的域名或IP地址
  
      location / {
          root /path/to/your/vue/project/dist; # 替换为你的Vue项目的dist目录的绝对路径
          index index.html;
          try_files $uri $uri/ /index.html;
      }
  
      error_page 500 502 503 504 /50x.html;
      location = /50x.html {
          root /usr/share/nginx/html;
      }
  }
  
  server {
      listen 8000;  # 监听端口 8000
      server_name localhost;
  
      location / {
          proxy_pass http://localhost:8000;  # 代理到 Django 后端
          proxy_http_version 1.1;
          proxy_set_header Upgrade $http_upgrade;
          proxy_set_header Connection 'upgrade';
          proxy_set_header Host $host;
          proxy_cache_bypass $http_upgrade;
      }
  }
  ```
  
  确保替换your_domain.com和/path/to/your/vue/project/dist为你的实际域名和Vue.js项目的实际路径。
  
- 前后端端口合一

  ```
      server {
          listen       3080;  # 监听端口 3080
          server_name localhost;
  
          location / {
              root /home/opsweb/opsClient/dist; # 替换为你的Vue项目的dist目录的绝对路径
              index index.html;
              try_files $uri $uri/ /index.html;
              # proxy_pass http://localhost:8000;  # 代理到 Django 后端
              # proxy_http_version 1.1;
              # proxy_set_header Upgrade $http_upgrade;
              # proxy_set_header Connection 'upgrade';
              # proxy_set_header Host $host;
              # proxy_cache_bypass $http_upgrade;
          }
          location /api/ {
              proxy_pass http://localhost:8000;
              proxy_set_header Host $host;
              proxy_set_header X-Real-IP $remote_addr;
              proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          }
          #error_page  404              /404.html;
  
          # redirect server error pages to the static page /50x.html
          #
          error_page   500 502 503 504  /50x.html;
          location = /50x.html {
              root   html;
          }
  
      }
  
  ```

  

## 重启NGINX

- 保存NGINX配置文件并重启NGINX以使更改生效：

  ```
  sudo service nginx restart
  ```

  或

  ```
  sudo systemctl restart nginx
  ```

  现在，你的Vue.js项目应该在NGINX上成功部署了。通过访问你的域名或服务器的IP地址，你应该能够看到你的Vue.js应用程序。

# 特殊用法记录

## 密码框校验规则

```javascript
const rules = {
      old_password: [{ required: true, message: '请输入原密码', trigger: 'blur' }
      ],
      password: [{ required: true, message: '请输入新密码', trigger: 'blur' },
      { pattern: /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,16}$/, message: '密码为8~16位且同时包含,数字+大小写字母+特殊符号', trigger: 'blur' }],
      password2: [{ required: true, message: '再一次新密码', trigger: 'blur' },
      { pattern: /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,16}$/, message: '密码为8~16位且同时包含,数字+大小写字母+特殊符号', trigger: 'blur' }],
    }
```

## 获取分页表格的展示数据

```javascript
    const getTableData = (init: boolean) => {
      if (init) {
        page.index = 1
      }
      tableData.value = []
      myTableData.value.forEach((value, index) => {
        // 0 20
        let min = (page.index - 1) * page.size
        // 19 39
        let max = (page.index - 1) * page.size + page.size - 1
        if (index >= min && index <= max) {
          tableData.value.push(value)
        }
      })
    }
    const myTableData = ref([])
```

