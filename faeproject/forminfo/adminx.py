import xadmin
from .models import *

# Register your models here.

class FormInfoPlanAdmin(object):
    list_display = ['fae_name','area','sellname','customer_name','number','customer_classification'\
    ,'project_name','start_date','reply_date','estimated_time','process','end_date','estimate',\
    'is_question','question_describe','satisfaction_score','satisfaction','transaction_time'\
    ,'customer_satisfaction']
    search_fields = ['fae_name','area','sellname']
    list_filter = ['start_date']
    # 关闭书签功能
    show_bookmarks = False
    # 修改图标
    model_icon = 'fa fa-cloud'
class FormInfoEventAdmin(object):
    list_display = ['fae_name','area','sellname','customer_name','customer_classification'\
    ,'project_name','start_date','reply_date','estimated_time','process','end_date','estimate',\
    'is_question','question_describe','satisfaction_score','satisfaction','transaction_time'\
    ,'customer_satisfaction']
    search_fields = ['fae_name','area','sellname']
    list_filter = ['start_date']
    # 关闭书签功能
    show_bookmarks = False
    # 修改图标
    model_icon = 'fa fa-cloud'
class FormInfoWorkAdmin(object):
    list_display = ['fae_name','area','sellname','demand','customer_name','customer_classification'\
    ,'start_date','estimated_time','process','end_date','estimate',\
    'is_question','question_describe','satisfaction_score','satisfaction','transaction_time']
    search_fields = ['fae_name','area','sellname']
    list_filter = ['start_date']
    # 关闭书签功能
    show_bookmarks = False
    # 修改图标
    model_icon = 'fa fa-cloud'

class CommentPlanAdmin(object):
    list_display = ['username','text','add_time','fae_name']
    search_fields = ['username','fae_name']
    list_filter = ['add_time']
    # 关闭书签功能
    show_bookmarks = False
    # 修改图标
    model_icon = 'fa fa-cloud'

class CommentEventAdmin(object):
    list_display = ['username','text','add_time','fae_name']
    search_fields = ['username','fae_name']
    list_filter = ['add_time']
    # 关闭书签功能
    show_bookmarks = False
    # 修改图标
    model_icon = 'fa fa-cloud'

class CommentWorkAdmin(object):
    list_display = ['username','text','add_time','fae_name']
    search_fields = ['username','fae_name']
    list_filter = ['add_time']
    # 关闭书签功能
    show_bookmarks = False
    # 修改图标
    model_icon = 'fa fa-cloud'

xadmin.site.register(FormInfoPlan,FormInfoPlanAdmin)
xadmin.site.register(FormInfoEvent,FormInfoEventAdmin)
xadmin.site.register(FormInfoWork,FormInfoWorkAdmin)
xadmin.site.register(CommentPlan,CommentPlanAdmin)
xadmin.site.register(CommentEvent,CommentEventAdmin)
xadmin.site.register(CommentWork,CommentWorkAdmin)