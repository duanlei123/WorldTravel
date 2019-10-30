from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import os

# Create your models here.


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return os.path.join('image', str(instance.id), filename)


class Myuser(AbstractUser):
    """
    用户表
    """
    nickname = models.CharField(max_length=50, verbose_name='昵称', default='')
    gender = models.CharField(max_length=6, verbose_name='性别', choices=(('male', '男'),
                                                                        ('female', '女'),
                                                                        ('secret', '保密')), default='secret')
    city_addr = models.CharField(max_length=6, verbose_name='居住地代码', default='410302')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日', default='1970-01-01')
    signature = models.CharField(max_length=300, verbose_name='个人签名', default='')
    portrait = models.ImageField(upload_to=user_directory_path, verbose_name='头像', default='image/default.jpg', max_length=100)
    integral = models.IntegerField(default=0, verbose_name='积分')
    check_time = models.DateField(default='1970-01-01', verbose_name='签到时间')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class TheContact(models.Model):
    """
    常用联系人表
    """
    user = models.ForeignKey(Myuser, verbose_name='用户', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, verbose_name='name', default='')
    city_addr = models.CharField(max_length=50, verbose_name='所在地区', default='')
    address = models.CharField(max_length=100, verbose_name='详细地址', default='')
    mobile = models.CharField(max_length=11, verbose_name='手机号', null=True, blank=True)
    zip_code = models.CharField(max_length=6, verbose_name='邮政编码', default='000000')
    is_default = models.BooleanField(verbose_name='是否默认')

    class Meta:
        verbose_name = '常用联系人信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class EmailVerifyRecord(models.Model):
    """
    邮箱验证码
    """
    code = models.CharField(max_length=80, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(choices=(('register', '注册'), ('find', '找回')), max_length=10, default='register', verbose_name='验证码类型')
    send_time = models.DateTimeField(default=datetime.now, verbose_name='发送时间')

    class Meta:
        verbose_name = '邮箱验证码信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)


class AreaInfo(models.Model):
    id = models.AutoField(auto_created=False, primary_key=True, serialize=False, verbose_name='ID')
    title = models.CharField(max_length=30, verbose_name='名称')
    Parent = models.ForeignKey('self', null=True, blank=True,on_delete=models.CASCADE, verbose_name='父级名称')