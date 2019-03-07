import xadmin
from .models import *

# Register your models here.

class ServiceAdmin(object):
    list_display = ['servicename','filltime','area','sellname','customer','faultdescription','faultrecord','faultresult',\
    'opinion','specificopinion','assistant1','assistant2','assistant3','assistant4']
    search_fields = ['servicename','area','sellname','customer']
    list_filter = ['filltime']
    # 关闭书签功能
    show_bookmarks = False
    # 修改图标
    model_icon = 'fa fa-cloud'


xadmin.site.register(Service,ServiceAdmin)