import datetime
import re
from django.db import models
from django.contrib.auth import models as auth_models
from identity.custom_validators.user import TechnologyValidator, MobileValidator
from django.conf import settings

__all__=[
    'User',
    'Group',
    'Permission',
    'UserActity'
]
# Create your models here.
##　自定义User表
class User(auth_models.AbstractUser):
    group = models.ManyToManyField('identity.Group', related_name='user_usergroup')
    user_permissions = models.ManyToManyField('identity.Permission', related_name='user_permission')
    department = models.CharField(max_length=50, verbose_name='部门')
    technology = models.CharField(max_length=8, verbose_name='员工编号',
                                  validators=[TechnologyValidator],unique=True)
    mobile = models.CharField(max_length=11, verbose_name='手机号',
                              validators=[MobileValidator],unique=True)
    jobs = models.CharField(max_length=50, verbose_name='工作岗位')

    class Meta:
        db_table = 'auth_user'
        default_permissions = []


class Group(auth_models.Group):
    """
    created=models.DateTimeField(auto_now_add=True)
    引起错误:?: (models.E017) Proxy model 'Group' contains model fields.
    问题解决:通过以上方法加字段添加到内置表中
            models.DateTimeField(auto_now_add=True).contribute_to_class(auth_models.Group,'created')
    """
    class Meta:
        proxy = True


class Permission(auth_models.Permission):
    """
    created=models.DateTimeField(auto_now_add=True)
    引起错误:?: (models.E017) Proxy model 'Permission' contains model fields.
                SystemCheckError: System check identified some issues:
    问题解决:通过以上方法加字段添加到内置表中
        models.DateTimeField(auto_now_add=True).contribute_to_class(auth_models.Permission,'created')
    """
    class Meta:
        proxy = True

models.DateTimeField(auto_now_add=True).contribute_to_class(auth_models.Group,'created')
models.CharField(max_length=50,verbose_name='隶属app',blank=True,null=True).contribute_to_class(auth_models.Group,'app')
models.DateTimeField(auto_now_add=True).contribute_to_class(auth_models.Permission,'created')

class UserActity(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    type=models.CharField(max_length=32,verbose_name='动作类型')
    created=models.DateTimeField(auto_now_add=True,verbose_name='操作时间')
    class Meta:
        default_permissions=[]
