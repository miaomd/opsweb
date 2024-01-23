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
    name=models.CharField(max_length=32,null=True,blank=True,verbose_name="姓名",default=' ')
    job_num=models.CharField(max_length=32,null=True,blank=True,verbose_name="工号",default=' ')
    role=models.CharField(choices=LEVEL,max_length=32,null=True,blank=True,verbose_name="用户角色")