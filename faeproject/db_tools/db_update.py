import sys
import os
#获取上一级文件的路径
cd = os.path.dirname(os.getcwd())
#添加需要导入的路径
sys.path.append(cd)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fae.settings")

import django
#调用此函数
django.setup()


from forminfo.models import FormInfoPlan , FormInfoEvent , FormInfoWork
from datetime import datetime
from datetime import timedelta
now_time = datetime.now()
last_time = now_time + timedelta(days=-14)
start = '2018-01-01'
last = last_time.strftime('%Y-%m-%d')
# 方案管理days天前
find_forminfoplan = FormInfoPlan.objects.filter(end_date__range=(start,last)).filter(is_question='')
find_forminfoplan.update(is_question='否',satisfaction_score='5',satisfaction='优秀',customer_satisfaction='优秀')
# 事件管理days天前
find_forminfoevent = FormInfoEvent.objects.filter(end_date__range=(start,last)).filter(is_question='')
find_forminfoevent.update(is_question='否',satisfaction_score='5',satisfaction='优秀',customer_satisfaction='优秀')
# 日常管理days天前
find_forminfowork = FormInfoWork.objects.filter(end_date__range=(start,last)).filter(is_question='')
find_forminfowork.update(is_question='否',satisfaction_score='5',satisfaction='优秀')
