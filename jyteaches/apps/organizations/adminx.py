import xadmin
from .models import CityDict,CourseOrg,Teacher


class CityDictAdmin(object):
    list_display = ['name','add_time']
    search_fields = ['name']
    list_filter = ['name']


class CourseOrgAdmin(object):
    list_display = ['name', 'click_nums','fav_nums','address','city']
    search_fields = ['name', 'city__name','address']
    list_filter = ['name', 'city','address']


class TeacherAdmin(object):
    list_display = ['name', 'courseorg', 'work_year','fav_nums','click_nums']
    search_fields = ['name', 'courseorg__name', 'work_year','fav_nums','click_nums']
    list_filter = ['name', 'courseorg', 'work_year','fav_nums','click_nums']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)
