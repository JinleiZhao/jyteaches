import xadmin
from .models import UserAsk,UserFav,UserMessage,CourseComments,UserCourse


class UserAskAdmin(object):
    list_display = ['name','mobile','coursename','add_time']
    search_fields = ['name','mobile','coursename']
    list_filter = ['name','mobile','coursename']


class UserFavAdmin(object):
    list_display = ['user', 'fav_type','add_time']
    search_fields = ['fav_type', 'user__username']
    list_filter = ['fav_type', 'user']


class UserMessageAdmin(object):
    list_display = ['user', 'has_read', 'add_time']
    search_fields = ['user', 'has_read']
    list_filter = ['user', 'has_read']


class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user__username', 'course__name']
    list_filter = ['user', 'course']


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user__username', 'course__name']
    list_filter = ['user', 'course']

xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserFav,UserFavAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(CourseComments,CourseCommentsAdmin)
xadmin.site.register(UserCourse,UserCourseAdmin)