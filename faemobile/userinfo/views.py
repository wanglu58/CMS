from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password
from django.db.models.aggregates import Count ,Avg,Sum
from .models import *
from forminfo.models import FormInfoPlan , FormInfoEvent , FormInfoWork
import logging
from django.http import HttpResponseRedirect
import time
import datetime
from datetime import timedelta
from django.db.models import Q
from Crypto import Random
from Crypto.Cipher import AES
import base64
from hashlib import md5

# Create myself views here.
def pad(data):
    length = 16 - (len(data) % 16)
    return data + (chr(length)*length).encode()

def unpad(data):
    return data[:-(data[-1] if type(data[-1]) == int else ord(data[-1]))]

def bytes_to_key(data, salt, output=48):
    assert len(salt) == 8, len(salt)
    data += salt
    key = md5(data).digest()
    final_key = key
    while len(final_key) < output:
        key = md5(key + data).digest()
        final_key += key
    return final_key[:output]

def encrypt(message, passphrase):
    salt = Random.new().read(8)
    key_iv = bytes_to_key(passphrase, salt, 32+16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(b"Salted__" + salt + aes.encrypt(pad(message)))

def decrypt(encrypted, passphrase):
    encrypted = base64.b64decode(encrypted)
    assert encrypted[0:8] == b"Salted__"
    salt = encrypted[8:16]
    key_iv = bytes_to_key(passphrase, salt, 32+16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(encrypted[16:]))

# Create myself views here.

# Create your views here.

def wel_1(request):
    # 时间
    now = datetime.datetime.now()
    last_week_start = now - timedelta(days=now.weekday()+7)
    last_week_end = now - timedelta(days=now.weekday()+1)
    this_month_start = datetime.datetime(now.year, now.month, 1)
    last_month_end = this_month_start - timedelta(days=1)
    laststart = last_week_start.strftime("%Y-%m-%d")
    lastend = last_week_end.strftime("%Y-%m-%d")
    thismonth = this_month_start.strftime("%m")
    lastmonth = last_month_end.strftime("%m")
    # 查询本月内的数据
    plan_month = UserInfo.objects.filter(forminfoplan__start_date__month=thismonth).annotate(num_plan=Sum('forminfoplan__number'))
    event_month = UserInfo.objects.filter(forminfoevent__start_date__month=thismonth).annotate(num_event=Count('forminfoevent'))
    work_month = UserInfo.objects.filter(forminfowork__start_date__month=thismonth).annotate(num_work=Count('forminfowork'))
    sale_plan_month = UserInfo.objects.filter(Q(forminfoplan__start_date__month=thismonth),Q(forminfoplan__is_question='是')|Q(forminfoplan__is_question='否')).annotate(num_saleplan=Count('forminfoplan'))
    sale_event_month = UserInfo.objects.filter(Q(forminfoevent__start_date__month=thismonth),Q(forminfoevent__is_question='是')|Q(forminfoevent__is_question='否')).annotate(num_saleevent=Count('forminfoevent'))
    sale_work_month = UserInfo.objects.filter(Q(forminfowork__start_date__month=thismonth),Q(forminfowork__is_question='是')|Q(forminfowork__is_question='否')).annotate(num_salework=Count('forminfowork'))
    sale_plan_month_score = UserInfo.objects.filter(forminfoplan__start_date__month=thismonth).annotate(score_plan=Avg('forminfoplan__satisfaction_score'))
    sale_event_month_score = UserInfo.objects.filter(forminfoevent__start_date__month=thismonth).annotate(score_event=Avg('forminfoevent__satisfaction_score'))
    sale_work_month_score = UserInfo.objects.filter(forminfowork__start_date__month=thismonth).annotate(score_work=Avg('forminfowork__satisfaction_score'))
    sale_plan_month_q =  UserInfo.objects.filter(Q(forminfoplan__start_date__month=thismonth),Q(forminfoplan__is_question='是')).annotate(num_saleplanq=Count('forminfoplan'))
    sale_event_month_q =  UserInfo.objects.filter(Q(forminfoevent__start_date__month=thismonth),Q(forminfoevent__is_question='是')).annotate(num_saleeventq=Count('forminfoevent'))
    sale_work_month_q =  UserInfo.objects.filter(Q(forminfowork__start_date__month=thismonth),Q(forminfowork__is_question='是')).annotate(num_saleworkq=Count('forminfowork'))
    
    data = {"plan_month":plan_month,"event_month":event_month,"work_month":work_month,\
    "sale_plan_month":sale_plan_month,"sale_event_month":sale_event_month,"sale_work_month":sale_work_month,\
    "sale_plan_month_score":sale_plan_month_score,"sale_event_month_score":sale_event_month_score,"sale_work_month_score":sale_work_month_score,\
    "sale_plan_month_q":sale_plan_month_q,"sale_event_month_q":sale_event_month_q,"sale_work_month_q":sale_work_month_q}
    return render(request,'welcome_1.html',data)

def wel_2(request):
    # 时间
    now = datetime.datetime.now()
    last_week_start = now - timedelta(days=now.weekday()+7)
    last_week_end = now - timedelta(days=now.weekday()+1)
    this_month_start = datetime.datetime(now.year, now.month, 1)
    last_month_end = this_month_start - timedelta(days=1)
    laststart = last_week_start.strftime("%Y-%m-%d")
    lastend = last_week_end.strftime("%Y-%m-%d")
    thismonth = this_month_start.strftime("%m")
    lastmonth = last_month_end.strftime("%m")
    # 查询上月内的数据
    plan_month = UserInfo.objects.filter(forminfoplan__start_date__month=lastmonth).annotate(num_plan=Sum('forminfoplan__number'))
    event_month = UserInfo.objects.filter(forminfoevent__start_date__month=lastmonth).annotate(num_event=Count('forminfoevent'))
    work_month = UserInfo.objects.filter(forminfowork__start_date__month=lastmonth).annotate(num_work=Count('forminfowork'))
    sale_plan_month = UserInfo.objects.filter(Q(forminfoplan__start_date__month=lastmonth),Q(forminfoplan__is_question='是')|Q(forminfoplan__is_question='否')).annotate(num_saleplan=Count('forminfoplan'))
    sale_event_month = UserInfo.objects.filter(Q(forminfoevent__start_date__month=lastmonth),Q(forminfoevent__is_question='是')|Q(forminfoevent__is_question='否')).annotate(num_saleevent=Count('forminfoevent'))
    sale_work_month = UserInfo.objects.filter(Q(forminfowork__start_date__month=lastmonth),Q(forminfowork__is_question='是')|Q(forminfowork__is_question='否')).annotate(num_salework=Count('forminfowork'))
    sale_plan_month_score = UserInfo.objects.filter(forminfoplan__start_date__month=lastmonth).annotate(score_plan=Avg('forminfoplan__satisfaction_score'))
    sale_event_month_score = UserInfo.objects.filter(forminfoevent__start_date__month=lastmonth).annotate(score_event=Avg('forminfoevent__satisfaction_score'))
    sale_work_month_score = UserInfo.objects.filter(forminfowork__start_date__month=lastmonth).annotate(score_work=Avg('forminfowork__satisfaction_score'))
    sale_plan_month_q =  UserInfo.objects.filter(Q(forminfoplan__start_date__month=lastmonth),Q(forminfoplan__is_question='是')).annotate(num_saleplanq=Count('forminfoplan'))
    sale_event_month_q =  UserInfo.objects.filter(Q(forminfoevent__start_date__month=lastmonth),Q(forminfoevent__is_question='是')).annotate(num_saleeventq=Count('forminfoevent'))
    sale_work_month_q =  UserInfo.objects.filter(Q(forminfowork__start_date__month=lastmonth),Q(forminfowork__is_question='是')).annotate(num_saleworkq=Count('forminfowork'))
    
    data = {"plan_month":plan_month,"event_month":event_month,"work_month":work_month,\
    "sale_plan_month":sale_plan_month,"sale_event_month":sale_event_month,"sale_work_month":sale_work_month,\
    "sale_plan_month_score":sale_plan_month_score,"sale_event_month_score":sale_event_month_score,"sale_work_month_score":sale_work_month_score,\
    "sale_plan_month_q":sale_plan_month_q,"sale_event_month_q":sale_event_month_q,"sale_work_month_q":sale_work_month_q}
    return render(request,'welcome_2.html',data)

def wel(request):
    # 时间
    now = datetime.datetime.now()
    last_week_start = now - timedelta(days=now.weekday()+7)
    last_week_end = now - timedelta(days=now.weekday()+1)
    this_month_start = datetime.datetime(now.year, now.month, 1)
    last_month_end = this_month_start - timedelta(days=1)
    laststart = last_week_start.strftime("%Y-%m-%d")
    lastend = last_week_end.strftime("%Y-%m-%d")
    thismonth = this_month_start.strftime("%m")
    lastmonth = last_month_end.strftime("%m")
    # 查询上周内的数据
    plan_week = UserInfo.objects.filter(forminfoplan__start_date__range=(laststart, lastend)).annotate(num_plan=Sum('forminfoplan__number'))
    event_week = UserInfo.objects.filter(forminfoevent__start_date__range=(laststart, lastend)).annotate(num_event=Count('forminfoevent'))
    work_week = UserInfo.objects.filter(forminfowork__start_date__range=(laststart, lastend)).annotate(num_work=Count('forminfowork'))
    sale_plan_week = UserInfo.objects.filter(Q(forminfoplan__start_date__range=(laststart, lastend)),Q(forminfoplan__is_question='是')|Q(forminfoplan__is_question='否')).annotate(num_saleplan=Count('forminfoplan'))
    sale_event_week = UserInfo.objects.filter(Q(forminfoevent__start_date__range=(laststart, lastend)),Q(forminfoevent__is_question='是')|Q(forminfoevent__is_question='否')).annotate(num_saleevent=Count('forminfoevent'))
    sale_work_week = UserInfo.objects.filter(Q(forminfowork__start_date__range=(laststart, lastend)),Q(forminfowork__is_question='是')|Q(forminfowork__is_question='否')).annotate(num_salework=Count('forminfowork'))
    sale_plan_week_score = UserInfo.objects.filter(forminfoplan__start_date__range=(laststart, lastend)).annotate(score_plan=Avg('forminfoplan__satisfaction_score'))
    sale_event_week_score = UserInfo.objects.filter(forminfoevent__start_date__range=(laststart,lastend)).annotate(score_event=Avg('forminfoevent__satisfaction_score'))
    sale_work_week_score = UserInfo.objects.filter(forminfowork__start_date__range=(laststart, lastend)).annotate(score_work=Avg('forminfowork__satisfaction_score'))
    sale_plan_week_q =  UserInfo.objects.filter(Q(forminfoplan__start_date__range=(laststart, lastend)),Q(forminfoplan__is_question='是')).annotate(num_saleplanq=Count('forminfoplan'))
    sale_event_week_q =  UserInfo.objects.filter(Q(forminfoevent__start_date__range=(laststart, lastend)),Q(forminfoevent__is_question='是')).annotate(num_saleeventq=Count('forminfoevent'))
    sale_work_week_q =  UserInfo.objects.filter(Q(forminfowork__start_date__range=(laststart, lastend)),Q(forminfowork__is_question='是')).annotate(num_saleworkq=Count('forminfowork'))
    
    data = {"plan_week":plan_week,"event_week":event_week,"work_week":work_week,\
    "sale_plan_week":sale_plan_week,"sale_event_week":sale_event_week,"sale_work_week":sale_work_week,\
    "sale_plan_week_score":sale_plan_week_score,"sale_event_week_score":sale_event_week_score,"sale_work_week_score":sale_work_week_score,\
    "sale_plan_week_q":sale_plan_week_q,"sale_event_week_q":sale_event_week_q,"sale_work_week_q":sale_work_week_q}
    return render(request,'welcome.html',data)

def homepage(request):
    return render(request,'homepage.html')

def index(request):
    if not request.session.get('user_name'):
        return render(request,'login.html')
    if request.session.get('user_name'):
        return HttpResponseRedirect("/index")


def index_(request):
    if not request.session.get('user_name'):
        return render(request,'login.html')
    # password_key = ".enginetech.cn.".encode()
    # ct_b64 = request.GET.get('pwd')
    # if not ct_b64:
    #     return render(request,'index.html')
    # try:
    #     ct_b64 = ct_b64.replace(' ','+')
    #     pt = decrypt(ct_b64, password_key)
    #     emid = pt.decode()
    #     if emid == str(9999):
    #         return HttpResponseRedirect("/boss")
    #     user = UserInfo()
    #     find_user = UserInfo.objects.filter(employeeid=emid)
    #     if not find_user:
    #         return render(request,'index.html')
    #     request.session['user_id'] = find_user[0].id
    #     request.session['user_name'] = find_user[0].username
    #     request.session['user_department'] = find_user[0].department
    # except Exception as e:
    #     logging.warning(e)
    #     return render(request, '404.html')
    return render(request, 'index.html')

def login_(request):
    return render(request, 'login.html')

def register_(request):
    return render(request, 'register.html')


def loginin(request):
    if request.method == 'POST':
        user = UserInfo()
        user.user = request.POST.get('username')
        user.password = request.POST.get('pwd')
        try:
            find_user = UserInfo.objects.filter(username=user.user)
            if not find_user:
                return render(request, 'login.html', {'message':'用户名不存在'})
            if find_user[0].isactive == 0:
                return render(request, 'login.html', {'message': '账户未激活，请联系管理员'})
            if find_user[0].error_number >= 5:
                endtime = datetime.datetime.now()
                starttime = find_user[0].updated_time
                if (endtime - starttime).seconds > 300 :
                    find_user[0].error_number = 0
                    find_user[0].save()
                    return render(request, 'login.html', {'message': '锁定已解除，请重新登录'})
                return  render(request,'login.html', {'message':"输错次数过多，账号已被锁定，请5分钟后重试"})
            if len(find_user) <= 0:
                return render(request,'login.html', {'message':'用户未注册'})
            if not check_password(user.password,find_user[0].userpassword):
                find_user[0].error_number += 1
                find_user[0].updated_time = datetime.datetime.now()
                find_user[0].save()
                return render(request,'login.html',{'message':'用户名或密码错误'})
        except ObjectDoesNotExist as e:
            logging.warning(e)
        request.session['user_id'] = find_user[0].id
        request.session['user_name'] = find_user[0].username
        request.session['user_department'] = find_user[0].department
        find_user[0].error_number = 0
        find_user[0].updated_time = datetime.datetime.now()
        find_user[0].save()
        return render(request,'index.html',{'message':'登录成功'})
    return render(request,'index.html')

def registerin(request):
    if request.method == 'POST':
        new_user = UserInfo()
        new_user.username = request.POST.get('username')
        new_user.username = new_user.username.replace(' ','')
        if new_user.username == '':
            return render(request,'register.html',{'message':'用户名不能为空'})
        if request.POST.get('gender') == '':
            return render(request,'register.html',{'message':'性别不能为空'})
        if request.POST.get('city') == '':
            return render(request,'register.html',{'message':'城市不能为空'})
        if request.POST.get('department') == '':
            return render(request,'register.html',{'message':'部门不能为空'})
        if request.POST.get('upwd') == '':
            return render(request,'register.html',{'message':'密码不能为空'})
        if request.POST.get('cpwd') == '':
            return render(request,'register.html',{'message':'密码不能为空'})
        if request.POST.get('employeeid') == '':
            return render(request,'register.html',{'message':'工号不能为空'})
        try:
            olduser = UserInfo.objects.filter(username=new_user.username)
            olduser1 = UserInfo.objects.filter(username=new_user.username+'1')
            olduser2 = UserInfo.objects.filter(username=new_user.username+'2')
            olduser3 = UserInfo.objects.filter(username=new_user.username+'3')
            olduser4 = UserInfo.objects.filter(username=new_user.username+'4')
            olduser5 = UserInfo.objects.filter(username=new_user.username+'5')
            if len(olduser) > 0:
                new_user.username = new_user.username + '1'
            if len(olduser1) > 0:
                new_user.username = new_user.username[:-1] + '2'
            if len(olduser2) > 0:
                new_user.username = new_user.username[:-1] + '3'
            if len(olduser3) > 0:
                new_user.username = new_user.username[:-1] + '4'
            if len(olduser4) > 0:
                new_user.username = new_user.username[:-1] + '5'
            if len(olduser5) > 0:
                return render(request,'login.html',{'message':'重名太多了吧，请联系管理员'})

        except ObjectDoesNotExist as e:
            logging.warning(e)
        
        upwd  = request.POST.get('upwd')
        cpwd = request.POST.get('cpwd')
        if len(upwd)<6 or len(upwd)>16 or len(cpwd)<6 or len(cpwd)>16:
            return render(request,'register.html',{'message':'密码必须6到16位，请重新输入'})
        if request.POST.get('upwd') != request.POST.get('cpwd'):
            return render(request,'register.html',{'message':'两次密码不一致，请重新输入'})
        new_user.userpassword = make_password(request.POST.get('upwd'), 'python', 'pbkdf2_sha1')
        new_user.gender = request.POST.get('gender')
        new_user.city = request.POST.get('city')
        new_user.department = request.POST.get('department')
        new_user.employeeid = request.POST.get('employeeid')
        try:
            new_user.save()
        except ObjectDoesNotExist as e:
            logging.warning(e)
        return render(request,'login.html',{'message':'注册成功','message1':'用户名：'+new_user.username})



def logout(request):
    #注销
    try:
        del request.session['user_id']
        del request.session['user_name']
        del request.session['user_department']
    except:
        pass
    try:
        if request.session['user_errortime']:
            del request.session['user_errortime']
    except:
        pass
    return render(request,'login.html')

def changepwd(request):
    return render(request, 'changepwd.html')

def change_pwd(request):
    if not request.session.get('user_name') :
        return render(request, 'login.html', {"message": "请先登录再修改密码！"})
    if request.method == "POST":
        user = UserInfo()
        user.name = request.POST.get("user_name")
        user.password = request.POST.get("old_password")
        if user.name == '':
            return render(request, 'changepwd.html', {'message': '用户名不能为空'})
        if user.password == '':
            return render(request, 'changepwd.html', {'message': '密码不能为空'})
        try:
            find_user = UserInfo.objects.filter(username=user.name)
            if not find_user:
                return render(request, 'changepwd.html', {'message':'用户名不存在'})
            if find_user[0].isactive == 0:
                if request.session.get('user_errortime'):
                    # print(request.session.get('user_errortime'))
                    if time.time() - request.session.get('user_errortime') >= 300:
                        find_user[0].isactive = 1
                        find_user[0].error_number = 0
                        find_user[0].save()
                        return render(request,'changepwd.html', {'message':'锁定已解除，请重新登录'})
                    else:
                        return render(request,'changepwd.html', {'message':'该账号已被锁定，请5分钟后重试'})
                return render(request, 'changepwd.html', {'message': '用户已被封禁'})
            if find_user[0].error_number >= 5:
                find_user[0].isactive = 0
                request.session['user_errortime'] = time.time()
                find_user[0].save()
                return  render(request,'changepwd.html', {'message':"输错次数过多，账号已被锁定，请5分钟后重试"})
            if len(find_user) <= 0:
                return render(request,'changepwd.html', {'message':'用户未注册'})
            if not check_password(user.password,find_user[0].userpassword):
                find_user[0].error_number += 1
                # print(find_user[0].error_number)
                find_user[0].save()
                return render(request,'changepwd.html',{'message':'用户名或密码错误'})
            if len(find_user) <= 0:
                return render(request, 'changepwd.html', {'message': '用户未注册'})
        except ObjectDoesNotExist as e:
            logging.warning(e)
        npwd  = request.POST.get('new_password')
        npwd1 = request.POST.get('new_password1')
        if len(npwd)<6 or len(npwd)>16 or len(npwd1)<6 or len(npwd1)>16:
            return render(request,'changepwd.html',{'message':'密码必须6到16位，请重新输入'})
        if request.POST.get('new_password') != request.POST.get('new_password1'):
            return render(request,'changepwd.html',{'message':'两次新密码不一致，请重新输入'})
        # if find_user[0].isdelete:
        #     return render(request,'changepwd.html',{'message':'用户不存在'})
        new_password = request.POST.get("new_password")
        update_user = UserInfo.objects.get(username=user.name)
        update_user.userpassword = make_password(new_password, 'python', 'pbkdf2_sha1')
        update_user.error_number = 0
        # print(update_user.userpassword)
        try:
            update_user.save()
        except ObjectDoesNotExist as e:
            logging.warning(e)
        return render(request, 'login.html', {'message': '密码修改成功'})
    else:
        return HttpResponseRedirect('/userinfo/login/')