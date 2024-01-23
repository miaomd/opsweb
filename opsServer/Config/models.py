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