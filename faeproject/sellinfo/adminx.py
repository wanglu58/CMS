import xadmin
from .models import *

# Register your models here.
class SellInfoWeeklyAdmin(object):
    list_display = ['sellname','filltime','salesamount','grossprofit','process','question','nextprocess']
    list_filter = ['filltime']
    search_fields = ['sellname']
    # 关闭书签功能
    show_bookmarks = False
    # 修改图标
    model_icon = 'fa fa-cloud'

class PipeLineAdmin(object):
    list_display = ['sellname','customer_name','customer_classification','project_name','advantage','keyperson','keypersonduties','phone'\
    ,'firsttime','demandtype','demandnumber','competitor','competitoradvantage','expected','process','winrate','filltime','planprocess','plantime']
    list_filter = ['filltime']
    search_fields = ['sellname','area','customer_name']
    # 关闭书签功能
    show_bookmarks = False
    # 修改图标
    model_icon = 'fa fa-cloud'

xadmin.site.register(SellInfoWeekly,SellInfoWeeklyAdmin)
xadmin.site.register(PipeLine,PipeLineAdmin)