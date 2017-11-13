from datetime import datetime
from django.db import models
from organizations.models import CourseOrg,Teacher


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='课程名字')
    desc = models.CharField(max_length=200,verbose_name='课程描述')
    detail = models.TextField(verbose_name='课程详情')
    courtime = models.IntegerField(default=0,verbose_name='课程时长')
    click_nums = models.IntegerField(default=0,verbose_name='点击次数')
    fav_nums = models.IntegerField(default=0,verbose_name='收藏此书')
    image = models.ImageField(upload_to='courses/%Y/%m',verbose_name='课程封面')
    studies = models.IntegerField(default=0,verbose_name='学习人数')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='登记时间')
    course_org = models.ForeignKey(CourseOrg,verbose_name='课程机构',null=True,blank=True)
    degree = models.CharField(max_length=20,choices=(('cj','初级'),('zj','中级'),('gj','高级')),verbose_name='课程难度',default='cj')
    category = models.CharField(max_length=30,verbose_name='课程类别',default='后台开发')
    tag = models.CharField(max_length=40,verbose_name='课程标签',default='服务器操作系统')
    annunciate = models.CharField(default='',verbose_name='课程通告',max_length=100)
    teacher = models.ForeignKey(Teacher,verbose_name='教师',null=True,blank=True)
    need_know = models.CharField(default='',verbose_name='课程须知',max_length=200)
    teacher_tell = models.CharField(default='',verbose_name='老师告诉你学到什么',max_length=200)

    class Meta:
        verbose_name = '课程详情'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_lesson_nums(self):  #计算课程外键的方法
        return self.lesson_set.all().count()

    def get_users(self):
        return self.usercourse_set.all()

    def get_lesson(self):
        return self.lesson_set.all()

    def get_resource(self):
        return self.courseresource_set.all()


class CourseResource(models.Model):
    name = models.CharField(max_length=50, verbose_name='资源名称')
    file = models.FileField(upload_to='courses/resource/%Y/%m',verbose_name='文件')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')
    course = models.ForeignKey(Course,verbose_name='对应课程')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=50,verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='登记时间')
    course = models.ForeignKey(Course,verbose_name='属于课程')

    class Meta:
        verbose_name = '章节详情'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name+self.course.name    #显示章节名加对应的课程

    def get_vidoe(self):
        return self.video_set.all()


class Video(models.Model):
    name = models.CharField(max_length=50,verbose_name='视频名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    lesson = models.ForeignKey(Lesson,verbose_name='对应章节')
    video = models.CharField(max_length=100,default='',verbose_name='视频地址')

    class Meta:
        verbose_name = '视频信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

