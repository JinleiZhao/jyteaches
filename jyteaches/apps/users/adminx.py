import xadmin
from .models import Banner,EmailVertifyRecord
from xadmin import views


class EmailVerifyRecordAdmin(object):
    pass


class BannerAdmin(object):
    list_display = ['title','url','index']

class BaseSetting( ):
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    site_title = "水浒传"
    site_footer = "游戏在线"
    menu_style = "accordion"

# xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(EmailVertifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)