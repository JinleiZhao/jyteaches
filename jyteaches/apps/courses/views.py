from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger   #分页
from operations.models import UserFav,CourseComments,UserCourse
from utils.mixin_utils import LoginRequireMixin
# Create your views here.
class CourseLisrView(View):
    def get(self,request):
        all_courses = Course.objects.all().order_by('-add_time')
        sort = request.GET.get('sort','')
        keywords = request.GET.get('keywords', '').strip()#去除字符出啊两边空格
        if keywords:
            all_courses = all_courses.filter(name__icontains=keywords)
        if sort:
            if sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')
            if sort == 'students':
                all_courses = all_courses.order_by('-studies')
        hot_courses = all_courses.order_by('click_nums')[:3]
        active = 'course'
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses,3,request=request)
                            #这里需要些一页显示几个
        all_courses = p.page(page)
        return render(request,'course-list.html',{
            'all_courses':all_courses,
            'sort':sort,
            'hot_courses':hot_courses,
            'active':active,
            'keywords':keywords,
        })

class CourseDetailView(View):
    def get(self,request,course_id):
        active = 'course'
        course = Course.objects.get(id=int(course_id))
        # users = course.get_users()
        # for cuser in users:
        #     img = cuser.user.image
        #course是usercourse的一个外键，user是usercourse的一个外键，所以需要cuser.user.image（不能直接cuser.image）
        tag = course.tag
        show_courses = Course.objects.filter(tag=tag)[:2]
        has_course_fav = False
        has_org_fav = False
        if request.user.is_authenticated:    #如果用户没有登陆则不执行收藏，若用户点击收藏则通过ajax返回到登路页面
            if UserFav.objects.filter(user=request.user,fav_id=int(course_id),fav_type=1):
                has_course_fav = True
            if UserFav.objects.filter(user=request.user,fav_id=int(course.course_org.id),fav_type=2):
                has_org_fav = True
        return render(request,'course-detail.html',{
            'course':course,
            'show_courses':show_courses,
            'has_course_fav':has_course_fav,
            'has_org_fav':has_org_fav,
            'course_id':course_id,
            'active': active,
        })

class CourseInfoView(LoginRequireMixin,View):
    def get(self,request,course_id):
        active = 'course'
        course = Course.objects.get(id=int(course_id))
        user = request.user
        if not UserCourse.objects.filter(course=course,user=user):  #如果没有匹配到数据，储存数据
            u_user = UserCourse(course=course, user=user)   #将数据存储到表中，等同于先实例化在存储
            u_user.save()
        user_courses = UserCourse.objects.filter(course=course)   #通过课程找到这个课程的用户集合
        user_course_ids = [user_course.user.id  for user_course in user_courses ]  #找到所有的该课程用户id
        all_user_courses = UserCourse.objects.filter(user_id__in=user_course_ids)  #通过用户id找到所有课程
        all_relative_courses = [user_course.course for user_course in all_user_courses]
        return render(request,'course-video.html',{
            'course_id':course_id,
            'course':course,
            'all_relative_courses':all_relative_courses,
            'active': active,
        })


class CourseCommentView(LoginRequireMixin,View):
    def get(self,request,course_id):
        active = 'course'
        course = Course.objects.get(id=int(course_id))
        user_courses = UserCourse.objects.filter(course=course)  # 通过课程找到这个课程的用户集合
        user_course_ids = [user_course.user.id for user_course in user_courses]  # 找到所有的该课程用户id
        all_user_courses = UserCourse.objects.filter(user_id__in=user_course_ids)  # 通过用户id找到所有课程
        all_relative_courses = [user_course.course for user_course in all_user_courses]
        course_comments = CourseComments.objects.filter(course=course).order_by('-add_time')
        return render(request,'course-comment.html',{
            'course':course,
            'course_comments':course_comments,
            'all_relative_courses': all_relative_courses,
            'active': active,
        })


class AddCommentView(View):
    def post(self,request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail"}',content_type='application/json')
        course_id = request.POST.get('course_id',0)
        comments = request.POST.get('comments','')
        if int(course_id)>0 and comments:
            course = Course.objects.get(id=int(course_id))
            course_comment = CourseComments()
            course_comment.user = request.user
            course_comment.course= course
            course_comment.comment = comments
            course_comment.save()
            return HttpResponse('{"status":"success","msg":"已收藏"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"已收藏"}', content_type='application/json')


