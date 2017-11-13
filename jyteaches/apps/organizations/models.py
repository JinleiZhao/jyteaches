from datetime import datetime
from django.db import models

# Create your models here.
class CityDict(models.Model):
    name = models.CharField(max_length=100,verbose_name='城市')
    desc = models.CharField(max_length=500,default='',verbose_name='描述')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = '城市信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=80,verbose_name="机构名字")
    desc = models.CharField(max_length=80,verbose_name="机构描述")
    students = models.IntegerField(default=0,verbose_name='学习人数')
    courses = models.IntegerField(default=0,verbose_name='课程数')
    org_category = models.CharField(max_length=20,choices=(('pxjg','培训机构'),('gx','高校'),('gr','个人')),verbose_name='机构类别',default='pxjg')
    click_nums = models.IntegerField(default=0, verbose_name="点击次数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏次数")
    image = models.ImageField(upload_to="courses/org/%Y/%m", verbose_name="机构图像")
    address = models.CharField(max_length=200,verbose_name="机构地址")
    city = models.ForeignKey(CityDict,verbose_name="机构城市")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return  self.name

    def get_teacher_nums(self):
        return self.teacher_set.all().count()

class Teacher(models.Model):
    courseorg = models.ForeignKey(CourseOrg,verbose_name="所属机构")
    name = models.CharField(max_length=30,verbose_name="讲师名字")
    work_year = models.IntegerField(default=0,verbose_name="工作年限")
    work_company = models.CharField(max_length=200,verbose_name="工作单位")
    work_position = models.CharField(max_length=100,verbose_name="工作职位")
    point = models.CharField(max_length=400,verbose_name="教学特点")
    click_nums = models.IntegerField(default=0, verbose_name="点击次数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏次数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    image = models.ImageField(upload_to="orgization/teacher/%Y/%m", verbose_name="教师头像",default='')
    age = models.IntegerField(default=18,verbose_name='年龄')

    class Meta:
        verbose_name = "讲师详情"
        verbose_name_plural = verbose_name

    def get_course(self):
        return self.course_set.all()

    def __str__(self):
        return self.name