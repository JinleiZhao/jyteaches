from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

#集成django自带的表，并在settings中进行覆盖
class  UserProfile(AbstractUser):
    nike_name = models.CharField(max_length=20,verbose_name='昵称')
    birthday = models.DateField(null=True,blank=True,verbose_name='生日')
    sex = models.CharField(choices=(('male','男'),('famale','女')),max_length=6,verbose_name='性别')
    mobile = models.IntegerField(max_length=11,verbose_name='手机号',null=True,blank=True)
    address = models.CharField(max_length=50,default='',verbose_name='地址')
    image = models.ImageField(upload_to='user/%Y/%m',max_length=500,verbose_name='头像')

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVertifyRecord(models.Model):
    code = models.CharField(max_length=10,verbose_name='验证码')
    email = models.EmailField(max_length=30,verbose_name='邮箱')
    send_type = models.CharField(choices=(('register','注册'),('forget','找回密码')),max_length=30,verbose_name='验证类型')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='时间')

    class Meta:
        verbose_name = '邮箱验证'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


class Banner(models.Model):
    title = models.CharField(max_length=10,verbose_name='标题')
    image = models.ImageField(upload_to='banner/%Y/%m',verbose_name='图像')
    url  = models.URLField(max_length=500,default='',verbose_name='跳转地址')
    index = models.IntegerField(default=100,verbose_name='顺序')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


