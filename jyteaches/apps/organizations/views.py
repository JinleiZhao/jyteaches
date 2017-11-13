from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .models import CityDict,CourseOrg,Teacher
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger   #分页
from .forms import UseraskForm
from operations.models import UserFav
from utils.mixin_utils import LoginRequireMixin
# Create your views here.

class orglist(View):
    def get(self,request):
        all_orgs= CourseOrg.objects.all()
        all_cities = CityDict.objects.all()
        keywords = request.GET.get('keywords', '').strip()#去除字符出啊两边空格
        if keywords:
            all_orgs = all_orgs.filter(name__icontains=keywords)
        sort_org = all_orgs.order_by('-click_nums')[:3]
        org_type = request.GET.get('ct','')                   #按机构
        if org_type:
            all_orgs = all_orgs.filter(org_category=org_type)
        city_id = request.GET.get('city','')                 #按城市
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
                                    #city是外键，通过外键id查找对应的数据，加上下划线
        sort = request.GET.get('sort','')    # 课程和学习人数排序
        active = 'org'
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-courses')

        all_nums = all_orgs.count()  #放在分页的前面，计算处理过的总的机构数
        #####################分页##############################
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs,4,request=request)
                            #这里需要些一页显示几个
        all_orgs = p.page(page)
        ######################################################
        return render(request,'org-list.html',{
            'all_orgs':all_orgs,
            'all_cities':all_cities,
            'all_nums':all_nums,
            'city_id':city_id,
            'org_type':org_type,
            'sort':sort,
            'sort_org':sort_org,
            'active':active,
            'keywords':keywords,
        })

class userask(View):
    def post(self,request):
        userask_form  = UseraskForm(request.POST)
        if userask_form.is_valid():
            userask_form.save(commit=True)#通过表单保存到数据库中
            return HttpResponse('{"status":"success"}',content_type='application/json')#以json格式提交
        else:
            return HttpResponse('{"status":"fail","msg":"提交失败"}',content_type='application/json')



class orghome(View):   #若想进入机构的详细信息则需要先进行登陆，否则无法获取到user则显示或报错
    def get(self,request,org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        courses = course_org.course_set.all()[:2] #外键反向查找
        teachers =course_org.teacher_set.all()[:3]
        org_fav = False
        login_user = request.user
        if request.user.is_authenticated:
            if UserFav.objects.filter(user=request.user,fav_id=int(org_id),fav_type=2):  #检查机构是否收藏
                org_fav = True
        current_page = 'home'
        return render(request,'org-detail-homepage.html',{
            'teachers':teachers,
            'courses':courses,
            'course_org':course_org,
            'org_id':org_id,
            'current_page':current_page,
            'org_fav':org_fav,
            'login_user':login_user,

        })


class orgcourse(View):
    def get(self,request,org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        courses = course_org.course_set.all() #外键反向查找
        current_page = 'course'
        org_fav = False
        if request.user.is_authenticated:
            if UserFav.objects.filter(user=request.user,fav_id=int(org_id),fav_type=2):  #检查机构是否收藏
                org_fav = True
        ######################分页#########################
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(courses,4,request=request)
                            #这里需要些一页显示几个
        courses = p.page(page)
        return render(request,'org-detail-course.html',{
            'courses':courses,
            'course_org':course_org,
            'org_id':org_id,
            'current_page':current_page,
            'org_fav': org_fav,
        })


class orgdesc(View):
    def get(self,request,org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        current_page = 'desc'
        org_fav = False
        if request.user.is_authenticated:
            if UserFav.objects.filter(user=request.user,fav_id=int(org_id),fav_type=2):  #检查机构是否收藏
                org_fav = True
        return render(request,'org-detail-desc.html',{
            'course_org':course_org,
            'org_id':org_id,
            'current_page':current_page,
            'org_fav': org_fav,
        })


class orgteacher(View):
    def get(self,request,org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        teachers = course_org.teacher_set.all()
        current_page = 'teacher'
        org_fav = False
        if request.user.is_authenticated:
            if UserFav.objects.filter(user=request.user,fav_id=int(org_id),fav_type=2):  #检查机构是否收藏
                org_fav = True
        return render(request,'org-detail-teachers.html',{
            'course_org':course_org,
            'org_id':org_id,
            'teachers':teachers,
            'current_page': current_page,
            'org_fav': org_fav,
        })

class user_fav(View):
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)
        fav_type  = request.POST.get('fav_type',0)

        if not request.user.is_authenticated(): #用户信息通过request传递
            return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type='application/json')
        exists_records = UserFav.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        if exists_records:
            exists_records.delete()#收藏存在删除
            return  HttpResponse('{"status":"success","msg":"收藏"}',content_type='application/json')
        else:
            user_fav = UserFav()
            if int(fav_id)>0 and int(fav_type)>0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"success","msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()
        hot_teacher = all_teachers.order_by('-click_nums')[:5]
        keywords = request.GET.get('keywords', '').strip()#去除字符出啊两边空格
        if keywords:
            all_teachers = all_teachers.filter(name__icontains=keywords)
            #                                 模糊匹配，类似sql语句中的like
        sort = request.GET.get('sort','')
        teacher_nums = all_teachers.count()
        active = 'teacher'
        if sort == 'hot':
            all_teachers = all_teachers.order_by('-click_nums')
        #########################分页########################
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers,4,request=request)
                            #这里需要些一页显示几个
        all_teachers = p.page(page)
        return render(request, 'teachers-list.html', {
            'all_teachers':all_teachers,
            'hot_teacher':hot_teacher,
            'sort':sort,
            'teacher_nums':teacher_nums,
            'active':active,
            'keywords':keywords,
        })


class TeacherDetailView(View):
    def get(self,request,teacher_id):
        active = 'teacher'
        teacher = Teacher.objects.get(id=int(teacher_id))
        hot_teacher = Teacher.objects.all().order_by('-click_nums')[:5]

        #############################判断是否收藏############################
        has_teacher_fav = False
        has_org_fav = False
        if request.user.is_authenticated:
            if UserFav.objects.filter(user=request.user,fav_id=int(teacher_id),fav_type=3):
                has_teacher_fav = True
            if UserFav.objects.filter(user=request.user,fav_id=int(teacher.courseorg.id),fav_type=3):
                has_org_fav = True
        ############################收藏操作在ajax中进行#####################
        return render(request,'teacher-detail.html',{
            'teacher':teacher,
            'hot_teacher':hot_teacher,
            'has_teacher_fav':has_teacher_fav,
            'has_org_fav':has_org_fav,
            'active':active,
        })