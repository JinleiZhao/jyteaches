"""jyteaches URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
import xadmin
from django.views.generic import  TemplateView
from users.views import user_login,user_register,user_active,forget_pwd,user_reset,user_reset_post,user_logout,index_view,UserCenterInfoView
from jyteaches.settings import MEDIA_ROOT,MEDIA_URL,STATIC_ROOT  #
from django.conf.urls.static import static            #引入media及static
from django.views.static import serve
from django.conf import settings


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    #url(r'^$',TemplateView.as_view(template_name='index.html'),name='index'),#不需要加视图函数
    url(r'^$',index_view.as_view(),name='index'),
    url(r'^login/$',user_login.as_view(),name='login'),
    url(r'logout/$',user_logout.as_view(),name='logout'),
    url(r'^register/$',user_register.as_view(),name='register'),
    url(r'^captcha',include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$',user_active.as_view(),name='active'),
    url(r'^forgetpwd/$',forget_pwd.as_view(),name='forgetpwd'),
    url(r'^reset/(?P<reset_code>.*)/$',user_reset.as_view(),name='reset'),
    url(r'^resetmodify/$',user_reset_post.as_view(),name='resetmodify'),
    url(r'^org/',include('organizations.urls',namespace='org')),
                                            #命名空间（在页面中能用org：xxx）
    url(r'^course/',include('courses.urls',namespace='course')),
    url(r'^user_info/$',UserCenterInfoView.as_view(),name='user_info'),

    url(r'^static/(?P<path>.*)$', serve, {'document_root':STATIC_ROOT}, name='static'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root':MEDIA_ROOT}, name='media'),
]+static(MEDIA_URL,document_root=MEDIA_ROOT)     #引入media
