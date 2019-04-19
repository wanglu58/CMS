import xadmin
from .models import *
from xadmin import views

# Register your models here.

class UserInfoAdmin(object):
    list_display = ['username','gender','city','department']
    search_fields = ['department','city','username','gender']
    # 关闭书签功能
    show_bookmarks = False
    # 修改图标
    model_icon = 'fa fa-user'
class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    # 添加更多主题
    # use_bootswatch = True

# 全局修改，固定写法
class GlobalSettings(object):
    # 修改title
    site_title = '安擎工作管理系统'
    # 修改footer
    site_footer = ' 安擎（天津）计算机有限公司'
    # 收起菜单
    # menu_style = 'accordion'

# Register your models here.
xadmin.site.register(UserInfo,UserInfoAdmin)
# 将基本配置管理与view绑定
xadmin.site.register(views.BaseAdminView,BaseSetting)
# 将title和footer信息进行注册
xadmin.site.register(views.CommAdminView,GlobalSettings)