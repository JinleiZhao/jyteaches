from django.shortcuts import render
from django.http import  HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile,EmailVertifyRecord,Banner
from django.db.models import Q
from django.views.generic import View
from .forms import Login_Form,Register_Form,ForgetPwd_Form,ResetPwd_Form,UserInfo_Form
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from organizations.models import CourseOrg,Teacher
from courses.models import Course
import json
from .forms import UploadImageForm
from utils.send_mail import register_send_mail
from operations.models import UserCourse,UserFav,UserMessage
from pure_pagination import Paginator, PageNotAnInteger   #分页

# Create your views here.


class CustomBackend(ModelBackend):   #重新定义这个类的authenticate这个方法，需要到settings注册
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))   #修改方法，username或者email等于usesrname
            if user.check_password(password):   #用django自带的方法对密码进行查询
                return user
        except:
            return  None


class user_login(View):
    def get(self,request):
        return render(request, 'login.html')
    def post(self,request):
        user_name = request.POST.get('username', '')
        pass_word = request.POST.get('password', '')
        login_form = Login_Form(request.POST)
        if login_form.is_valid():    #先用form表单进行验证，减少对数据库的操作
            user = authenticate(username=user_name, password=pass_word)  #通过django自带的方法，去与数据库中的数据进行验证
            if user is not None:
                if user.is_active:
                    login(request, user)
                    #return render(request, 'index.html')
                    # from django.core.urlresolvers import reverse
                    # return HttpResponseRedirect(reverse("index"))
                    return HttpResponseRedirect('/')
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码有误'})
        else:
            return render(request, 'login.html',{'login_form':login_form})

# def user_login(request):
#     if request.method == 'GET':
#         return render(request,'login.html')
#     elif request.method == 'POST':
#         user_name = request.POST.get('username','')
#         pass_word = request.POST.get('password','')
#         user = authenticate(username=user_name,password=pass_word)
#         if user is not None:
#             login(request,user)
#             return render(request,'index.html')
#         else:
#             return render(request,'login.html',{'msg':'用户名有误'})

class user_register(View):
    def get(self,request):
        register_form = Register_Form()
        return render(request,'register.html',{'register_form':register_form})
    def post(self,request):
        register_form = Register_Form(request.POST)
        #print(register_form)
        if register_form.is_valid():
            email =  request.POST.get('email','')
            password = request.POST.get('password','')
            user_email = UserProfile.objects.filter(email=email)
            if user_email:
                return render(request,'register.html',{'msg':'邮箱已经存在','register_form':register_form})
            else:
                user_profile = UserProfile()
                user_profile.username = email
                user_profile.email = email
                user_profile.is_active = False   #新注册用户处于不激活状态
                user_profile.password = make_password(password)
                user_profile.save()
                register_send_mail(email,send_type='register')
                return render(request,'login.html')
            #Duplicate entry '1120886306@qq.com' for key 'username
        else:
            return render(request,'register.html',{'register_form':register_form})


class user_active(View):
    def get(self,request,active_code):
        email_recodes = EmailVertifyRecord.objects.filter(code=active_code)
        if email_recodes:
            for recode in email_recodes:
                user = UserProfile.objects.get(email=recode.email)
                user.is_active = True
                user.save()
            return render(request,'login.html')
        else:
            return HttpResponse('链接无效')


class forget_pwd(View):
    def get(self,request):
        forgetpwd_form = ForgetPwd_Form()
        return render(request,'forgetpwd.html',{'forgetpwd_form':forgetpwd_form})
    def post(self,request):
        forgetpwd_form = ForgetPwd_Form(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get('email','')
            email_exists = UserProfile.objects.filter(email=email).count()
            if email_exists  == 0:
                show_content = '{"account":"邮箱不存在"}'
            else:
                register_send_mail(email, send_type='forget')
                show_content = '{"status":"success"}'
            return HttpResponse(show_content,content_type='application/json')
        else:
            return HttpResponse('{"captcha_f":"验证码不正确"}',content_type='application/json')

class user_reset(View):    #通过邮件直接进入到这个类，因为传递了参数所以post提交另创建一个类(user_reset_post)
    def get(self,request,reset_code):
        reset_email = EmailVertifyRecord.objects.get(code=reset_code).email  #通过code值获取Email传到前端，在post后返回作为修改的用户
        return render(request,'password_reset.html',{'email':reset_email})

class user_reset_post(View):
    def post(self,request):
        resetpwd_form = ResetPwd_Form(request.POST)
        email = request.POST.get('email', '')   #每次提交时都要获取一遍email值传递给下次，否则下次得到的Email值为空
        if resetpwd_form.is_valid():
            passwd1 = request.POST.get('password1','')
            passwd2 = request.POST.get('password2',' ')
            if passwd1 == passwd2:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(passwd1)
                user.save()
                return  render(request,'login.html')
            else:
                return render(request,'password_reset.html',{'msg':'两次密码不一样','email':email})
        else:
            return render(request,'password_reset.html',{'msg':"输入有误",'email':email})

class user_logout(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect('/')      #跳转重定向
        #return render(request,'index.html')   #加载模板


class index_view(View):
    def get(self,request):
        active = ''
        all_banners = Banner.objects.all().order_by("index")
        courses = Course.objects.filter()[:5]
        banner_courses = Course.objects.filter()[:3]
        course_orgs = CourseOrg.objects.all()[:5]
        return render(request, "index.html", {
            "all_banners": all_banners,
            "courses": courses,
            "banner_courses": banner_courses,
            "course_orgs": course_orgs,
            'active':active,
        })

class UserCenterInfoView(View):
    def get(self,request):
        user = request.user
        content = 'info'
        return render(request,'usercenter-info.html',{
            'user':user,
            'content': content,
        })
    def post(self,request):
        user_info_form = UserInfo_Form(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status": "success", "msg":"修改成功"}', content_type="application/json")
        else:
            # message = '{"status": "failure"}'
            return HttpResponse( json.dumps(user_info_form.errors),content_type="application/json")

class UploadImageView(View):
    """
     用户修改头像
     """
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            userprofile = UserProfile()
            userprofile.image = request.FILES
            userprofile.save()
            return HttpResponse('{"status": "success", "msg":"修改成功"}', content_type="application/json")
        else:
            return HttpResponse('{"status": "fail", "msg":"修改失败"}', content_type="application/json")

class UpdatePwdView(View):
    """
    个人中心密码修改
    """
    def post(self,request):
        modify_form = ResetPwd_Form(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status": "fail", "msg":"修改失败"}', content_type="application/json")
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status": "success", "msg":"修改成功"}', content_type="application/json")
        else:
            return HttpResponse('{"msg":"密码不能少于6位"}',content_type="application/json")


class SendEamilCodeView(View):
    """
    发送邮箱验证码
    """
    def get(self, request):
        email = request.GET.get("email", "")
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email": "邮箱已存在"}', content_type="application/json")
        register_send_mail(email, "update_email")
        return HttpResponse('{"status": "success", "msg":"修改成功"}', content_type="application/json")

class UpdateEmailView( View):
    """
        修改个人邮箱
        """
    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")

        existed_codes = EmailVertifyRecord.objects.filter(email=email, code=code, send_type="update_email")
        if existed_codes:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status": "success", "msg":"修改成功"}', content_type="application/json")
        else:
            return HttpResponse('{"email": "验证码出错"}', content_type="application/json")


class MyCourseView(View):
    """
    我的课程
    """
    def get(self, request):
        content = 'course'
        user_courses = UserCourse.objects.filter(user_id=request.user.id)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(user_courses,3, request=request)
        # 这里需要些一页显示几个
        user_courses = p.page(page)
        return render(request, "usercenter-mycourse.html", {
            "user_courses": user_courses,
            'content': content,
        })


class MyFavOrgView(View):
    """
    我收藏的课程机构
    """
    def get(self, request):
        org_list = []
        content = 'org'
        myfav = 'org'
        fav_orgs = UserFav.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, "usercenter-fav-org.html", {
            "org_list": org_list,
            'myfav': myfav,
            'content': content,
        })


class MyFavTeacherView(View):
    """
    我收藏的授课讲师
    """
    def get(self, request):
        teacher_list = []
        content = 'org'
        myfav = 'teacher'
        fav_teachers = UserFav.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, "usercenter-fav-teacher.html", {
            "teacher_list": teacher_list,
            'myfav': myfav,
            'content': content,
        })


class MyFavCourseView(View):
    """
    我收藏的课程
    """
    def get(self, request):
        course_list = []
        content = 'org'
        myfav = 'course'
        fav_courses = UserFav.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, "usercenter-fav-course.html", {
            "course_list": course_list,
            'myfav':myfav,
            'content':content,
        })

class MyMessageView(View):
    """
    我的消息
    """
    def get(self, request):
        content = 'message'
        all_messages = UserMessage.objects.filter(user=request.user.id)
        all_unread_message = UserMessage.objects.filter(user=request.user.id,has_read=False)
        for unread_message in all_unread_message:
            unread_message.has_read = True
            unread_message.save()

        return render(request, "usercenter-message.html", {
            "all_messages":all_messages,
            'content':content,
        })
