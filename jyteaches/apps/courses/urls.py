from django.conf.urls import url
from jyteaches.settings import MEDIA_ROOT,MEDIA_URL   #
from django.conf.urls.static import static            #引入media及static
from .views import CourseLisrView,CourseDetailView,CourseInfoView,CourseCommentView,AddCommentView

urlpatterns = [

    url(r'^course_list/$',CourseLisrView.as_view(),name='course_list'),
    url(r'^course_detail/(?P<course_id>.*)/$',CourseDetailView.as_view(),name='course_detail'),
    url(r'course_video/(?P<course_id>.*)/$',CourseInfoView.as_view(),name='course_video'),
    url(r'course_comment/(?P<course_id>.*)/$',CourseCommentView.as_view(),name='course_comment'),
    url(r'add_comment/$',AddCommentView.as_view(),name='add_comment'),
]+static(MEDIA_URL,document_root=MEDIA_ROOT)     #引入media