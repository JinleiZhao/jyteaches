from django.conf.urls import url,include
from jyteaches.settings import MEDIA_ROOT,MEDIA_URL   #
from django.conf.urls.static import static            #引入media及static
from organizations.views import orglist,userask,orghome,orgcourse,orgdesc,orgteacher,user_fav,TeacherListView,TeacherDetailView

urlpatterns = [
    url(r'^orglist/$',orglist.as_view(),name='orglist'),
    url(r'^userask/$',userask.as_view(),name='userask'),
    url(r'^orghome/(?P<org_id>.*)/$',orghome.as_view(),name='orghome'),  #(?P<org_id>.*)这部分内容写错，当在前端引入url时会报错
    url(r'^orgcourse/(?P<org_id>.*)/$',orgcourse.as_view(),name='orgcourse'),
    url(r'^orgdesc/(?P<org_id>.*)/$',orgdesc.as_view(),name='orgdesc'),
    url(r'^orgteacher/(?P<org_id>.*)/$',orgteacher.as_view(),name='orgteacher'),
    url(r'^add_fav/$',user_fav.as_view(),name='add_fav'),
    url(r'^teacher_list/$',TeacherListView.as_view(),name='teacher_list'),
    url(r'teacher_detail/(?P<teacher_id>.*)/$',TeacherDetailView.as_view(),name='teacher_detail'),
]+static(MEDIA_URL,document_root=MEDIA_ROOT)     #引入media