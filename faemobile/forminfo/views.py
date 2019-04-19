from django.shortcuts import render
from .models import *
from django.db.models import Q
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect , HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
import xlwt
from io import *
import xlrd
from django import forms
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.db import transaction
import time
import datetime
from datetime import timedelta
from django.utils.http import urlquote
# Create your views here.

def excelplan(request):
    return render(request, 'excelplan.html')

def excelevent(request):
    return render(request, 'excelevent.html')

def excelwork(request):
    return render(request, 'excelwork.html')

def showplaninfo(request):
    # 方案展示
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        project_id = request.GET.get('project_id')[:-1]
        form_detailone = FormInfoPlan.objects.filter(id=project_id)
        return render(request,'showplaninfo.html',{'form_detailone':form_detailone})

def showeventinfo(request):
    # 事件展示
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        project_id = request.GET.get('project_id')[:-1]
        form_detailone = FormInfoEvent.objects.filter(id=project_id)
        return render(request,'showeventinfo.html',{'form_detailone':form_detailone})

def showworkinfo(request):
    # 工作展示
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        project_id = request.GET.get('project_id')[:-1]
        form_detailone = FormInfoWork.objects.filter(id=project_id)
        return render(request,'showworkinfo.html',{'form_detailone':form_detailone})

def info_plan(request):
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    form_id = request.session.get('user_id')
    form_user = request.session.get('user_name')
    try:
        #找到该用户填写的方案表单
        if request.session.get('user_department') == "整机事业部" or request.session.get('user_department') =="渠道事业部":
            find_forminfoplan = FormInfoPlan.objects.filter(Q(username=form_id) | Q(sellname=form_user)).order_by("-id")
        if request.session.get('user_department') != "整机事业部" and request.session.get('user_department') != "渠道事业部":
            find_forminfoplan = FormInfoPlan.objects.filter(username=form_id).order_by("-id")
        if request.session.get('user_name') == "陈武" :
            find_forminfoplan = FormInfoPlan.objects.filter(username__department__contains='技术部').order_by("-id")
        #分页
        paginatorplan = Paginator(find_forminfoplan,20,1)
        pageplan = request.GET.get('page')
        try:
            formsplan = paginatorplan.page(pageplan)
        except PageNotAnInteger:
            formsplan = paginatorplan.page(1)
        except EmptyPage:
            formsplan = paginatorplan.page(paginatorplan.num_pages)
        if request.method == "POST":
            if request.session.get('user_name') != "陈武" :
                if request.POST.get('show_timeplan') != '' and request.POST.get('show_timeevent') != '':
                    showtimestart = request.POST.get('show_timeplan')
                    showtimeend = request.POST.get('show_timeevent')
                    # 找到所有该时间段用户填写的方案表单
                    if request.session.get('user_department') == "整机事业部" or request.session.get('user_department') =="渠道事业部":
                        find_forminfoplan = FormInfoPlan.objects.filter(Q(username=form_id) | Q(sellname=form_user)).filter(start_date__range=(showtimestart,showtimeend)).order_by("-id")
                    if request.session.get('user_department') != "整机事业部" and request.session.get('user_department') != "渠道事业部":
                        find_forminfoplan  = FormInfoPlan.objects.filter(username=form_id).filter(start_date__range=(showtimestart,showtimeend)).order_by("-id")
                    return render(request,'plansearch.html',{'Forminfoplan':find_forminfoplan})
                return render(request,'plan.html',{'Forminfoplan':formsplan})
            show_name = request.POST.get('show_name')
            show_area = request.POST.get('show_area')
            show_sellname = request.POST.get('show_sellname')
            showtimestart = request.POST.get('show_timeplan')
            # request.session['upshowtimestart'] = showtimestart
            showtimeend = request.POST.get('show_timeevent')
            search_dict =dict()
            if show_name :
                search_dict['fae_name__contains'] = show_name
            if show_area :
                search_dict['area__contains'] = show_area
            if show_sellname :
                search_dict['sellname__contains'] = show_sellname
            if not search_dict:
                if not showtimestart or not showtimeend: 
                    return render(request,'plan.html',{'Forminfoplan':formsplan})
            if request.session.get('user_name') == "陈武" :
                if showtimestart !='' and showtimeend != '':
                    find_forminfoplan = FormInfoPlan.objects.filter(**search_dict).filter(start_date__range=(showtimestart,showtimeend)).filter(username__department__contains='技术部').order_by("-id")
                if showtimestart == '' or showtimeend == '':
                    find_forminfoplan = FormInfoPlan.objects.filter(**search_dict).filter(username__department__contains='技术部').order_by("-id")
            return render(request,'plansearch.html',{'Forminfoplan':find_forminfoplan})
        return render(request,'plan.html',{'Forminfoplan':formsplan})
    except Exception as e:
        logging.warning(e)
        return HttpResponse("系统有误!")
    


def info_event(request):
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    form_id = request.session.get('user_id')
    form_user = request.session.get('user_name')
    try:
        #找到该用户填写的事件表单
        if request.session.get('user_department') == "整机事业部" or request.session.get('user_department') =="渠道事业部":
            find_forminfoevent = FormInfoEvent.objects.filter(Q(username=form_id) | Q(sellname=form_user)).order_by("-id")
        if request.session.get('user_department') != "整机事业部" and request.session.get('user_department') != "渠道事业部":
            find_forminfoevent = FormInfoEvent.objects.filter(username=form_id).order_by("-id")
        if request.session.get('user_name') == "陈武" :
            find_forminfoevent = FormInfoEvent.objects.filter(username__department__contains='技术部').order_by("-id")
        #分页
        paginatorevent = Paginator(find_forminfoevent,20,1)
        pageevent = request.GET.get('page')
        try:
            formsevent = paginatorevent.page(pageevent)
        except PageNotAnInteger:
            formsevent = paginatorevent.page(1)
        except EmptyPage:
            formsevent = paginatorevent.page(paginatorevent.num_pages)
        if request.method == "POST":
            # dict = request.POST
            if request.session.get('user_name') != "陈武" :
                if request.POST.get('show_timeplan') != '' and request.POST.get('show_timeevent') != '':
                    showtimestart = request.POST.get('show_timeplan')
                    showtimeend = request.POST.get('show_timeevent')
                    # 找到所有该时间段用户填写的事件表单
                    if request.session.get('user_department') == "整机事业部" or request.session.get('user_department') =="渠道事业部":
                        find_forminfoevent = FormInfoEvent.objects.filter(Q(username=form_id) | Q(sellname=form_user)).filter(start_date__range=(showtimestart,showtimeend)).order_by("-id")
                    if request.session.get('user_department') != "整机事业部" and request.session.get('user_department') !="渠道事业部":
                        find_forminfoevent = FormInfoEvent.objects.filter(username=form_id).filter(start_date__range=(showtimestart,showtimeend)).order_by("-id")
                    return render(request, 'eventsearch.html', {'Forminfoevent': find_forminfoevent})
                return render(request, 'event.html', {'Forminfoevent': formsevent})
            show_name = request.POST.get('show_name')
            show_area = request.POST.get('show_area')
            show_sellname = request.POST.get('show_sellname')
            showtimestart = request.POST.get('show_timeplan')
            showtimeend = request.POST.get('show_timeevent')
            search_dict =dict()
            if show_name :
                search_dict['fae_name__contains'] = show_name
            if show_area :
                search_dict['area__contains'] = show_area
            if show_sellname :
                search_dict['sellname__contains'] = show_sellname
            if not search_dict:
                if not showtimestart or not showtimeend:
                    return render(request,'event.html',{'Forminfoevent':formsevent})
            if request.session.get('user_name') == "陈武" :
                if showtimestart !='' and showtimeend != '':
                    find_forminfoevent = FormInfoEvent.objects.filter(**search_dict).filter(start_date__range=(showtimestart,showtimeend)).filter(username__department__contains='技术部').order_by("-id")
                if showtimestart == '' or showtimeend == '':
                    find_forminfoevent = FormInfoEvent.objects.filter(**search_dict).filter(username__department__contains='技术部').order_by("-id")
            return render(request, 'eventsearch.html', {'Forminfoevent': find_forminfoevent})
        return render(request, 'event.html', {'Forminfoevent': formsevent})

    except Exception as e:
        logging.warning(e)
        return HttpResponse("系统有误!")


def info_work(request):
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    form_id = request.session.get('user_id')
    form_user = request.session.get('user_name')
    try:
        #找到该用户填写的事件表单
        if request.session.get('user_department') == "整机事业部" or request.session.get('user_department') =="渠道事业部":
            find_forminfowork = FormInfoWork.objects.filter(Q(username=form_id) | Q(sellname=form_user)).order_by("-id")
        if request.session.get('user_department') != "整机事业部" and request.session.get('user_department') !="渠道事业部":
            find_forminfowork = FormInfoWork.objects.filter(username=form_id).order_by("-id")
        if request.session.get('user_name') == "陈武" :
            find_forminfowork = FormInfoWork.objects.filter(username__department__contains='技术部').order_by("-id")
        #分页
        paginatorwork = Paginator(find_forminfowork,20,1)
        pagework = request.GET.get('page')
        try:
            formswork = paginatorwork.page(pagework)
        except PageNotAnInteger:
            formswork = paginatorwork.page(1)
        except EmptyPage:
            formswork = paginatorwork.page(paginatorwork.num_pages)
        if request.method == "POST":
            # dict = request.POST
            if request.session.get('user_name') != "陈武" :
                if request.POST.get('show_timeplan') != '' and request.POST.get('show_timeevent') != '':
                    showtimestart = request.POST.get('show_timeplan')
                    showtimeend = request.POST.get('show_timeevent')
                    # 找到所有该时间段用户填写的事件表单
                    if request.session.get('user_department') == "整机事业部" or request.session.get('user_department') =="渠道事业部":
                        find_forminfowork = FormInfoWork.objects.filter(Q(username=form_id) | Q(sellname=form_user)).filter(start_date__range=(showtimestart,showtimeend)).order_by("-id")
                    if request.session.get('user_department') != "整机事业部" and request.session.get('user_department') !="渠道事业部":
                        find_forminfowork = FormInfoWork.objects.filter(username=form_id).filter(start_date__range=(showtimestart,showtimeend)).order_by("-id")
                    return render(request, 'worksearch.html', {'Forminfowork': find_forminfowork})
                return render(request, 'work.html', {'Forminfowork': formswork})
            show_name = request.POST.get('show_name')
            show_area = request.POST.get('show_area')
            show_sellname = request.POST.get('show_sellname')
            showtimestart = request.POST.get('show_timeplan')
            showtimeend = request.POST.get('show_timeevent')
            search_dict =dict()
            if show_name :
                search_dict['fae_name__contains'] = show_name
            if show_area :
                search_dict['area__contains'] = show_area
            if show_sellname :
                search_dict['sellname__contains'] = show_sellname
            if not search_dict:
                if not showtimestart or not showtimeend:
                    return render(request,'work.html',{'Forminfowork':formswork})
            if request.session.get('user_name') == "陈武" :
                if showtimestart !='' and showtimeend != '':
                    find_forminfowork = FormInfoWork.objects.filter(**search_dict).filter(start_date__range=(showtimestart,showtimeend)).filter(username__department__contains='技术部').order_by("-id")
                if showtimestart == '' or showtimeend == '':
                    find_forminfowork = FormInfoWork.objects.filter(**search_dict).filter(username__department__contains='技术部').order_by("-id")
            return render(request, 'worksearch.html', {'Forminfowork': find_forminfowork})
        return render(request, 'work.html', {'Forminfowork': formswork})

    except Exception as e:
        logging.warning(e)
        return HttpResponse("系统有误!")

def addinfo_plan(request):
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    return render(request, 'addformplan.html')
def addinfo_event(request):
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    return render(request, 'addformevent.html')

def addinfo_work(request):
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    return render(request, 'addformwork.html')

def addinfoplan_(request):
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        if request.method == "POST":
            # 获取前端发来的表单信息
            new_info = FormInfoPlan()
            new_info.fae_name = request.POST.get('fae_name')
            # print(new_info)
            new_info.area = request.POST.get('area')
            new_info.sellname = request.POST.get('sellname')
            new_info.customer_name = request.POST.get('customer_name')
            new_info.number = request.POST.get('number')
            new_info.customer_classification = request.POST.get('customer_classification')
            new_info.project_name = request.POST.get('project_name')
            new_info.start_date = request.POST.get('start_date')
            new_info.reply_date = request.POST.get('reply_date')
            new_info.estimated_time = request.POST.get('estimated_time')
            new_info.process = request.POST.get('process')
            new_info.end_date = request.POST.get('end_date')
            new_info.estimate = request.POST.get('estimate')
            # new_info.is_question = request.POST.get('is_question')
            # new_info.question_describe = request.POST.get('question_describe')
            # new_info.satisfaction_score = request.POST.get('satisfaction_score')
            # new_info.satisfaction = request.POST.get('satisfaction')
            # if request.POST.get('transaction_time') != '':
            #     new_info.transaction_time = request.POST.get('transaction_time')
            # new_info.customer_satisfaction = request.POST.get('customer_satisfaction')
            new_info.username = UserInfo.objects.get(id=request.session.get('user_id'))
            try:
                new_info.save()
            except Exception as e:
                logging.warning(e)
                return HttpResponse("输入格式有误!")
            return HttpResponseRedirect('/forminfo/plan/')
        else:
            return HttpResponseRedirect('/forminfo/plan/')


def addinfoevent_(request):
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        if request.method == "POST":
            # 获取前端发来的表单信息
            new_info = FormInfoEvent()
            new_info.fae_name = request.POST.get('fae_name')
            new_info.area = request.POST.get('area')
            new_info.sellname = request.POST.get('sellname')
            new_info.customer_name = request.POST.get('customer_name')
            # new_info.number = request.POST.get('number')
            new_info.customer_classification = request.POST.get('customer_classification')
            new_info.project_name = request.POST.get('project_name')
            new_info.start_date = request.POST.get('start_date')
            new_info.reply_date = request.POST.get('reply_date')
            new_info.estimated_time = request.POST.get('estimated_time')
            new_info.process = request.POST.get('process')
            new_info.end_date = request.POST.get('end_date')
            new_info.estimate = request.POST.get('estimate')
            # new_info.is_question = request.POST.get('is_question')
            # new_info.question_describe = request.POST.get('question_describe')
            # new_info.satisfaction_score = request.POST.get('satisfaction_score')
            # new_info.satisfaction = request.POST.get('satisfaction')
            # if request.POST.get('transaction_time') != '':
            #     new_info.transaction_time = request.POST.get('transaction_time')
            # new_info.customer_satisfaction = request.POST.get('customer_satisfaction')
            new_info.username = UserInfo.objects.get(id=request.session.get('user_id'))
            try:
                new_info.save()
            except Exception as e:
                logging.warning(e)
                return HttpResponse("输入格式有误!")
            return HttpResponseRedirect('/forminfo/event/')
        else:
            return HttpResponseRedirect('/forminfo/event/')

def addinfowork_(request):
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        if request.method == "POST":
            # 获取前端发来的表单信息
            new_info = FormInfoWork()
            new_info.fae_name = request.POST.get('fae_name')
            new_info.area = request.POST.get('area')
            new_info.sellname = request.POST.get('sellname')
            new_info.demand = request.POST.get('demand')
            new_info.customer_name = request.POST.get('customer_name')
            new_info.customer_classification = request.POST.get('customer_classification')
            new_info.start_date = request.POST.get('start_date')
            new_info.estimated_time = request.POST.get('estimated_time')
            new_info.process = request.POST.get('process')
            new_info.end_date = request.POST.get('end_date')
            new_info.estimate = request.POST.get('estimate')
            new_info.username = UserInfo.objects.get(id=request.session.get('user_id'))
            try:
                new_info.save()
            except Exception as e:
                logging.warning(e)
                return HttpResponse("输入格式有误!")
            return HttpResponseRedirect('/forminfo/work/')
        else:
            return HttpResponseRedirect('/forminfo/work/')


def revise_plan(request):
    if not request.session.get('user_name'):
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        if request.session.get('user_department') == "整机事业部" or request.session.get('user_department') == "渠道事业部":
            # 寻找只属于此销售的方案表单
            exclusiveform = FormInfoPlan.objects.filter(sellname=request.session.get('user_name')).order_by("-id")
            # print(request.session.get('user_name'))
            # return render(request, "showinfolistplan.html", {'exclusiveform':exclusiveform})
            # 分页
            paginatorplan = Paginator(exclusiveform,20,1)
            pageplan = request.GET.get('page')
            try:
                formsplan = paginatorplan.page(pageplan)
            except PageNotAnInteger:
                formsplan = paginatorplan.page(1)
            except EmptyPage:
                formsplan = paginatorplan.page(paginatorplan.num_pages)
            if request.method == "POST":
            #获取前端发来的查询信息
                dict = request.POST
                if dict.get('show_timeplan') and dict.get('show_timeevent') != '':
                    showtimestart = dict.get('show_timeplan')
                    showtimeend = dict.get('show_timeevent')
                    exclusiveform = FormInfoPlan.objects.filter(sellname=request.session.get('user_name')).filter(start_date__range=(showtimestart,showtimeend)).order_by("-id")
                    return render(request, "showinfolistplan.html", {'exclusiveform':exclusiveform})
            return render(request, 'showinfolistplan.html', {'exclusiveform': formsplan})
        return render(request, 'showinfolistplan.html', {'cannotfind': '没有找到指定你评价的项目。'})

def amend_plan(request):
    if not request.session.get('user_name'):
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        if request.session.get('user_department') != "整机事业部" and request.session.get('user_department') != "渠道事业部":
            form_id = request.session.get('user_id')
            # form_user = request.session.get('user_name')
            #找到该用户填写的方案表单
            find_forminfoplan = FormInfoPlan.objects.filter(username=form_id).order_by("-id")
            #分页
            paginatorplan = Paginator(find_forminfoplan,20,1)
            pageplan = request.GET.get('page')
            try:
                formsplan = paginatorplan.page(pageplan)
            except PageNotAnInteger:
                formsplan = paginatorplan.page(1)
            except EmptyPage:
                formsplan = paginatorplan.page(paginatorplan.num_pages)
            if request.method == "POST":
                dict = request.POST
                if dict.get('show_timeplan') and dict.get('show_timeevent') != '':
                    showtimestart = dict.get('show_timeplan')
                    showtimeend = dict.get('show_timeevent')
                    # 找到所有该时间段用户填写的方案表单
                    find_forminfoplan = FormInfoPlan.objects.filter(username=form_id).filter(start_date__range=(showtimestart,showtimeend)).order_by("-id")
                    return render(request, 'amendplan.html',{'exclusiveform':find_forminfoplan})
            return render(request, 'amendplan.html',{'exclusiveform': formsplan})
        return render(request, 'amendplan.html' ,{'cannotfind':'您目前无权利修改！'})

def amend_event(request):
    if not request.session.get('user_name'):
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        if request.session.get('user_department') != "整机事业部" and request.session.get('user_department') != "渠道事业部":
            form_id = request.session.get('user_id')
            find_forminfoevent = FormInfoEvent.objects.filter(username=form_id).order_by("-id")
            #分页
            paginatorevent = Paginator(find_forminfoevent,20,1)
            pageevent = request.GET.get('page')
            try:            # form_user = request.session.get('user_name')
            #找到该用户填写的事件管理

                formsevent = paginatorevent.page(pageevent)
            except  PageNotAnInteger:
                formsevent = paginatorevent.page(1)
            except EmptyPage:
                formsevent = paginatorevent.page(paginatorevent.num_pages)
            if request.method == "POST":
                dict = request.POST
                if dict.get('show_timeplan') and dict.get('show_timeevent') != '':
                    showtimestart = dict.get('show_timeplan')
                    showtimeend = dict.get('show_timeevent')
                    # 找到所有该时间段用户填写的事件表单
                    find_forminfoevent = FormInfoEvent.objects.filter(username=form_id).filter(start_date__range=(showtimestart,showtimeend)).order_by("-id")
                    return render(request,'amendevent.html',{'exclusiveform':find_forminfoevent})
            return render(request,'amendevent.html',{'exclusiveform': formsevent})
        return render(request, 'amendevent.html',{'cannotfind':'您目前无权利修改！'})


def amend_work(request):
    if not request.session.get('user_name'):
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        if request.session.get('user_department') != "整机事业部" and request.session.get('user_department') != "渠道事业部":
            form_id = request.session.get('user_id')
            #找到该用户填写的日常管理
            find_forminfowork = FormInfoWork.objects.filter(username=form_id).order_by("-id")
            #分页
            paginatorwork = Paginator(find_forminfowork,20,1)
            pagework = request.GET.get('page')
            try:
                formswork = paginatorwork.page(pagework)
            except PageNotAnInteger:
                formswork = paginatorwork.page(1)
            except EmptyPage:
                formswork = paginatorwork.page(paginatorwork.num_pages)
            if request.method == "POST":
                dict = request.POST
                if dict.get('show_timeplan') and dict.get('show_timeevent') != '':
                    showtimestart = dict.get('show_timeplan')
                    showtimeend = dict.get('show_timeevent')
                    # 找到所有该时间段用户填写的日常表单
                    find_forminfowork = FormInfoWork.objects.filter(username=form_id).filter(start_date__range=(showtimestart,showtimeend)).order_by("-id")
                    return render(request,'amendwork.html',{'exclusiveform':find_forminfowork})
            return render(request,'amendwork.html',{'exclusiveform': formswork})
        return render(request, 'amendwork.html',{'cannotfind':'您目前无权利修改！'})

def revise_event(request):
    if not request.session.get('user_name'):
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        if request.session.get('user_department') == "整机事业部" or request.session.get('user_department') == "渠道事业部":
            # 寻找只属于此销售的事件表单
            exclusiveform = FormInfoEvent.objects.filter(sellname=request.session.get('user_name')).order_by("-id")
            # print(request.session.get('user_name'))
            # return render(request, "showinfolistevent.html", {'exclusiveform':exclusiveform})
            #分页
            paginatorplan = Paginator(exclusiveform,20,1)
            pageplan = request.GET.get('page')
            try:
                formsplan = paginatorplan.page(pageplan)
            except PageNotAnInteger:
                formsplan = paginatorplan.page(1)
            except EmptyPage:
                formsplan = paginatorplan.page(paginatorplan.num_pages)
            if request.method == "POST":
            #获取前端发来的查询信息
                dict = request.POST
                if dict.get('show_timeplan') and dict.get('show_timeevent') != '':
                    showtimestart = dict.get('show_timeplan')
                    showtimeend = dict.get('show_timeevent')
                    exclusiveform = FormInfoEvent.objects.filter(sellname=request.session.get('user_name')).filter(start_date__range=(showtimestart,showtimeend)).order_by("-id")
                    return render(request, 'showinfolistevent.html', {'exclusiveform':exclusiveform})
            return render(request, 'showinfolistevent.html', {'exclusiveform':formsplan})
        return render(request, 'showinfolistevent.html', {'cannotfind': '没有找到指定你评价的项目。'})

def revise_work(request):
    if not request.session.get('user_name'):
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        if request.session.get('user_department') == "整机事业部" or request.session.get('user_department') == "渠道事业部":
            # 寻找只属于此销售的日常表单
            exclusiveform = FormInfoWork.objects.filter(sellname=request.session.get('user_name')).order_by("-id")
            # 分页
            paginatorwork = Paginator(exclusiveform,20,1)
            pagework = request.GET.get('page')
            try:
                formswork = paginatorwork.page(pagework)
            except PageNotAnInteger:
                formswork = paginatorwork.page(1)
            except EmptyPage:
                formswork = paginatorwork.page(paginatorwork.num_pages)
            if request.method == "POST":
            # 获取前端发来的查询信息
                dict = request.POST
                if dict.get('show_timeplan') and dict.get('show_timeevent') != '':
                    showtimestart = dict.get('show_timeplan')
                    showtimeend = dict.get('show_timeevent')
                    exclusiveform = FormInfoWork.objects.filter(sellname=request.session.get('user_name')).filter(start_date__range=(showtimestart,showtimeend)).order_by("-id")
                    return render(request, 'showinfolistwork.html', {'exclusiveform':exclusiveform})             
            return render(request, 'showinfolistwork.html', {'exclusiveform':formswork})
        return render(request, 'showinfolistwork.html', {'cannotfind': '没有找到指定你评价的项目。'})

def show_plandetail(request):
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        # 修改界面展示
        project_id = request.GET.get('project_planid')[:-1]
        form_detailone = FormInfoPlan.objects.filter(id=project_id)
        request.session['form_id'] = project_id
        return render(request, 'changeinfoplan.html', {'form_detailone':form_detailone})

def amendplaninfo_(request):
    if not request.session.get('user_name'):
        return render(request, 'unlogin.html',{"message":"先右上角登录再操作"})
    else:
        #修改界面展示
        project_id = request.GET.get('project_planid')[:-1]
        form_detailone = FormInfoPlan.objects.filter(id=project_id)
        request.session['form_id'] = project_id
        return render(request, 'amendplanshow.html', {'form_detailone':form_detailone})

def amendeventinfo_(request):
    if not request.session.get('user_name'):
        return render(request, 'unlogin.html',{"message":"先右上角登录再操作"})
    else:
        #修改界面展示
        project_id = request.GET.get('project_eventid')[:-1]
        form_detailone = FormInfoEvent.objects.filter(id=project_id)
        request.session['form_id'] = project_id
        return render(request, 'amendeventshow.html', {'form_detailone':form_detailone})

def amendworkinfo_(request):
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        #修改页面展示
        project_id = request.GET.get('project_workid')[:-1]
        form_detailone = FormInfoWork.objects.filter(id=project_id)
        request.session['form_id'] = project_id
        return render(request, 'amendworkshow.html', {'form_detailone':form_detailone})

def show_eventdetail(request):
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        # 修改界面展示
        project_id = request.GET.get('project_eventid')[:-1]
        form_detailone = FormInfoEvent.objects.filter(id=project_id)
        request.session['form_id'] = project_id
        return render(request, 'changeinfoevent.html', {'form_detailone':form_detailone})

def show_workdetail(request):
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        # 修改界面展示
        project_id = request.GET.get('project_workid')[:-1]
        form_detailone = FormInfoWork.objects.filter(id=project_id)
        request.session['form_id'] = project_id
        return render(request, 'changeinfowork.html', {'form_detailone':form_detailone})

def update_workform(request):
    # 修改
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        if request.method == "POST":
            times = request.POST.get('transaction_time')
            if times == '':
                times = None
            project_id = request.session.get('form_id')
            update_info = FormInfoWork.objects.get(id=project_id)
            update_info.is_question = request.POST.get('is_question')
            update_info.question_describe = request.POST.get('question_describe')
            update_info.satisfaction_score = request.POST.get('satisfaction_score')
            update_info.satisfaction = request.POST.get('satisfaction')
            update_info.transaction_time = times
            try:
                update_info.save()
            except Exception as e:
                logging.warning(e)
                return HttpResponse("输入格式有误!")
            del request.session['form_id']
            return HttpResponseRedirect('/forminfo/workrevise/')
        else:
            return HttpResponseRedirect('/forminfo/work/')

def update_planform(request):
    # 修改
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        if request.method == "POST":
            times = request.POST.get('transaction_time')
            if times == '':
                times = None
            project_id = request.session.get('form_id')
            # print(project_id)
            update_info = FormInfoPlan.objects.get(id=project_id)
            update_info.is_question = request.POST.get('is_question')
            update_info.question_describe = request.POST.get('question_describe')
            update_info.satisfaction_score = request.POST.get('satisfaction_score')
            update_info.satisfaction = request.POST.get('satisfaction')
            update_info.transaction_time = times
            update_info.customer_satisfaction = request.POST.get('customer_satisfaction')
            try:
                update_info.save()
            except Exception as e:
                logging.warning(e)
                return HttpResponse("输入格式有误!")
            del request.session['form_id']
            return HttpResponseRedirect('/forminfo/planrevise/')
        else:
            return HttpResponseRedirect('/forminfo/plan/')

def amendplaninfoshow_(request):
    # 修正
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        if request.method == "POST":
            project_id = request.session.get('form_id')
            update_info = FormInfoPlan.objects.get(id=project_id)
            update_info.fae_name = request.POST.get('fae_name')
            update_info.area = request.POST.get('area')
            update_info.sellname = request.POST.get('sellname')
            update_info.customer_name = request.POST.get('customer_name')
            update_info.number = request.POST.get('number')
            update_info.customer_classification =request.POST.get('customer_classification')
            update_info.project_name = request.POST.get('project_name')
            update_info.start_date = request.POST.get('start_date')
            update_info.reply_date = request.POST.get('reply_date')
            update_info.estimated_time = request.POST.get('estimated_time')
            update_info.process = request.POST.get('process')
            update_info.end_date = request.POST.get('end_date')
            update_info.estimate = request.POST.get('estimate')
            try:
                update_info.save()
            except Exception as e:
                logging.warning(e)
                return HttpResponse("输入格式有误!")
            del request.session['form_id']
            return HttpResponseRedirect('/forminfo/amend-plan/')
        else:
            return HttpResponseRedirect('/forminfo/plan')

def amendeventinfoshow_(request):
    #修正
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        if request.method == "POST":
            project_id = request.session.get('form_id')
            update_info = FormInfoEvent.objects.get(id=project_id)
            update_info.fae_name = request.POST.get('fae_name')
            update_info.area = request.POST.get('area')
            update_info.sellname = request.POST.get('sellname')
            update_info.customer_name = request.POST.get('customer_name')
            update_info.customer_classification = request.POST.get('customer_classification')
            update_info.project_name = request.POST.get('project_name')
            update_info.start_date = request.POST.get('start_date')
            update_info.reply_date = request.POST.get('reply_date')
            update_info.estimated_time = request.POST.get('estimated_time')
            update_info.process = request.POST.get('process')
            update_info.end_date = request.POST.get('end_date')
            update_info.estimate = request.POST.get('estimate')
            try:
                update_info.save()
            except Exception as e:
                logging.warning(e)
                return HttpResponse("输入格式有误!")
            del request.session['form_id']
            return HttpResponseRedirect('/forminfo/amend-event/')
        else:
            return HttpResponseRedirect('/forminfo/event')


def amendworkinfoshow_(request):
    #修正
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        if request.method == "POST":
            project_id = request.session.get('form_id')
            update_info = FormInfoWork.objects.get(id=project_id)
            update_info.fae_name = request.POST.get('fae_name')
            update_info.area = request.POST.get('area')
            update_info.sellname = request.POST.get('sellname')
            update_info.demand = request.POST.get('demand')
            update_info.customer_name = request.POST.get('customer_name')
            update_info.customer_classification = request.POST.get('customer_classification')
            update_info.start_date = request.POST.get('start_date')
            update_info.estimated_time = request.POST.get('estimated_time')
            update_info.process = request.POST.get('process')
            update_info.end_date = request.POST.get('end_date')
            update_info.estimate = request.POST.get('estimate')
            try:
                update_info.save()
            except Exception as e:
                logging.warning(e)
                return HttpResponse("输入格式有误!")
            del request.session['form_id']
            return HttpResponseRedirect('/forminfo/amend-work/')
        else:
            return HttpResponseRedirect('/forminfo/work')

def update_eventform(request):
    # 修改
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        if request.method == "POST":
            times = request.POST.get('transaction_time')
            if times == '':
                times = None
            # print(project_id)
            project_id = request.session.get('form_id')
            update_info = FormInfoEvent.objects.get(id=project_id)
            update_info.is_question = request.POST.get('is_question')
            update_info.question_describe = request.POST.get('question_describe')
            update_info.satisfaction_score = request.POST.get('satisfaction_score')
            update_info.satisfaction = request.POST.get('satisfaction')
            update_info.transaction_time = times
            update_info.customer_satisfaction = request.POST.get('customer_satisfaction')
            try:
                update_info.save()
            except Exception as e:
                logging.warning(e)
                return HttpResponse("输入格式有误!")
            del request.session['form_id']
            return HttpResponseRedirect('/forminfo/eventrevise/')
        else:
            return HttpResponseRedirect('/forminfo/event/')

#以下仅测试代码
# def forminfo_(request):
#     if not request.session.get('user_name') :
#         return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
#     form_id = request.session.get('user_id')
#     form_user = request.session.get('user_name')
#     try:
#         # 找到所有该用户填写的表单
#         find_forminfoplan = FormInfoPlan.objects.filter(Q(username=form_id) | Q(sellname=form_user))
#         find_forminfoevent = FormInfoEvent.objects.filter(Q(username=form_id) | Q(sellname=form_user))
#         # print(find_forminfoplan)
#         if request.method == "POST":
#             dict = request.POST
#             if dict.get('show_timeplan') and dict.get('show_timeevent') != '':
#                 showtimestart = dict.get('show_timeplan')
#                 showtimeend = dict.get('show_timeevent')
#                 # 找到所有该时间段用户填写的表单
#                 find_forminfoplan = FormInfoPlan.objects.filter(Q(username=form_id) | Q(sellname=form_user)).filter(start_date__range=(showtimestart,showtimeend))
#                 find_forminfoevent = FormInfoEvent.objects.filter(Q(username=form_id) | Q(sellname=form_user)).filter(start_date__range=(showtimestart,showtimeend))
#                 return render(request, 'forminfo.html', {'Forminfoplan': find_forminfoplan,
#                       'Forminfoevent': find_forminfoevent})

#             return render(request, 'forminfo.html', {'Forminfoplan': find_forminfoplan,
#                       'Forminfoevent': find_forminfoevent})
#         return render(request, 'forminfo.html', {'Forminfoplan': find_forminfoplan,
#                       'Forminfoevent': find_forminfoevent})

#     except ObjectDoesNotExist as e:
#         logging.warning(e)
#以上仅测试代码

def export_excelplan(request):
    # 设置HttpResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = "attachment;filename=FaePlan.xls"
    # 新建一个文件
    wb = xlwt.Workbook(encoding='utf-8')
    # 新建一个sheet
    sheet = wb.add_sheet('方案管理')
    # 样式
    style_heading = xlwt.easyxf("""
        font:
            name 宋体,
            color-index red,
            bold on;
        """
        )
    style_body = xlwt.easyxf("""
        font:
            name 宋体;
        """
        )
    style_num = xlwt.easyxf("""
        font:
            name 宋体;
    """
        )
    style_num.num_format_str = 'yyyy/m/d'

    # 写标题栏
    sheet.write(0,0,'FAE姓名', style_heading)
    sheet.write(0,1,'区域 ', style_heading)
    sheet.write(0,2,'销售', style_heading)
    sheet.write(0,3,'客户名称', style_heading)
    sheet.write(0,4,'数量', style_heading)
    sheet.write(0,5,'客户分类', style_heading)
    sheet.write(0,6,'项目名称', style_heading)
    sheet.write(0,7,'发起时间', style_heading)
    sheet.write(0,8,'要求回复时间', style_heading)
    sheet.write(0,9,'预计用时   ', style_heading)
    sheet.write(0,10,'过程描述', style_heading)
    sheet.write(0,11,'结束时间', style_heading)
    sheet.write(0,12,'用时估算', style_heading)
    sheet.write(0,13,'是否有问题', style_heading)
    sheet.write(0,14,'问题描述', style_heading)
    sheet.write(0,15,'满意度评分', style_heading)
    sheet.write(0,16,'评价', style_heading)
    sheet.write(0,17,'成交时间', style_heading)
    sheet.write(0,18,'客户满意度', style_heading)

    #写数据
    form_id = request.session.get('user_id')
    form_user = request.session.get('user_name')
    if request.method == "POST":
        show_name = request.POST.get('show_name')
        # request.session['upshow_name'] = show_name
        show_area = request.POST.get('show_area')
        # request.session['upshow_area'] = show_area
        show_sellname = request.POST.get('show_sellname')
        # request.session['upshow_sellname'] = show_sellname
        showtimestart = request.POST.get('show_timeplan')
        # request.session['upshowtimestart'] = showtimestart
        showtimeend = request.POST.get('show_timeevent')
        # request.session['upshowtimeend'] = showtimeend
        # print(show_name)
        search_dict =dict()
        if show_name :
            search_dict['fae_name__contains'] = show_name
        if show_area :
            search_dict['area__contains'] = show_area
        if show_sellname :
            search_dict['sellname__contains'] = show_sellname
        if request.session.get('user_name') == "陈武" :
            if showtimestart != '' and showtimeend != '':
                find_forminfoplan = FormInfoPlan.objects.filter(**search_dict).filter(start_date__range=(showtimestart,showtimeend)).filter(username__department__contains='技术部').order_by("id")
            if showtimestart == '' or showtimeend == '':
                find_forminfoplan = FormInfoPlan.objects.filter(**search_dict).filter(username__department__contains='技术部').order_by("id")
        if request.session.get('user_name') != "陈武" :
            if showtimestart != '' and showtimeend != '':
                if request.session.get('user_department') == "整机事业部" or request.session.get('user_department') =="渠道事业部":
                    find_forminfoplan = FormInfoPlan.objects.filter(Q(username=form_id) | Q(sellname=form_user)).filter(start_date__range=(showtimestart,showtimeend)).order_by("id")
                if request.session.get('user_department') != "整机事业部" and request.session.get('user_department') != "渠道事业部":
                    find_forminfoplan  = FormInfoPlan.objects.filter(username=form_id).filter(start_date__range=(showtimestart,showtimeend)).order_by("id")
            if showtimestart == '' or showtimeend == '':
                if request.session.get('user_department') == "整机事业部" or request.session.get('user_department') =="渠道事业部":
                    find_forminfoplan = FormInfoPlan.objects.filter(Q(username=form_id) | Q(sellname=form_user)).order_by("id")
                if request.session.get('user_department') != "整机事业部" and request.session.get('user_department') != "渠道事业部":
                    find_forminfoplan  = FormInfoPlan.objects.filter(username=form_id).order_by("id")
        row = 1
        for info in find_forminfoplan:
            sheet.write(row,0,info.fae_name,style_body)
            sheet.write(row,1,info.area,style_body)
            sheet.write(row,2,info.sellname,style_body)
            sheet.write(row,3,info.customer_name,style_body)
            sheet.write(row,4,info.number,style_body)
            sheet.write(row,5,info.customer_classification,style_body)
            sheet.write(row,6,info.project_name,style_body)
            # 调整宽度
            sheet.col(7).width = 3000
            sheet.write(row,7,info.start_date,style_num)
            try:
                replydate = int(info.reply_date)
            except Exception as e:
                # logging.warning(e)
                replydate = info.reply_date
            sheet.write(row,8,replydate,style_body)
            sheet.write(row,9,info.estimated_time,style_body)
            sheet.write(row,10,info.process,style_body)
            # 调整宽度
            sheet.col(11).width = 3000
            sheet.write(row,11,info.end_date,style_num)
            sheet.write(row,12,info.estimate,style_body)
            sheet.write(row,13,info.is_question,style_body)
            sheet.write(row,14,info.question_describe,style_body)
            sheet.write(row,15,info.satisfaction_score,style_body)
            sheet.write(row,16,info.satisfaction,style_body)
            # 调整宽度
            sheet.col(17).width = 3000
            sheet.write(row,17,info.transaction_time,style_num)
            sheet.write(row,18,info.customer_satisfaction,style_body)
            row = row + 1
        #写出到io
        output = BytesIO()
        wb.save(output)
        #重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
        return response
    return render(request, '404.html')

def export_excelplan_question(request):
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    form_id = request.session.get('user_id')
    form_user = request.session.get('user_name')
    try:
        #找到该用户填写的方案表单
        if request.session.get('user_department') != "整机事业部" and request.session.get('user_department') != "渠道事业部":
            find_forminfoplan = FormInfoPlan.objects.filter(username=form_id).filter(is_question="是").order_by("-id")
        if request.session.get('user_name') == "陈武" :
            find_forminfoplan = FormInfoPlan.objects.filter(username__department__contains='技术部').filter(is_question="是").order_by("-id")
        #分页
        paginatorplan = Paginator(find_forminfoplan,20,1)
        pageplan = request.GET.get('page')
        try:
            formsplan = paginatorplan.page(pageplan)
        except PageNotAnInteger:
            formsplan = paginatorplan.page(1)
        except EmptyPage:
            formsplan = paginatorplan.page(paginatorplan.num_pages)
        return render(request,'planquestion.html',{'Forminfoplan':formsplan})
    except Exception as e:
        logging.warning(e)
        return HttpResponse("系统有误!")



def export_excelevent(request):
    # 设置HttpResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = "attachment;filename=FaeEvent.xls"
    # 新建一个文件
    wb = xlwt.Workbook(encoding='utf-8')
    # 新建一个sheet
    sheet = wb.add_sheet('事件管理')
    # 样式
    style_heading = xlwt.easyxf("""
        font:
            name 宋体,
            color-index red,
            bold on;
        """
        )
    style_body = xlwt.easyxf("""
        font:
            name 宋体;
        """
        )

    style_num = xlwt.easyxf("""
        font:
            name 宋体;
    """
        )
    style_num.num_format_str = 'yyyy/m/d'

    # 写标题栏
    sheet.write(0,0,'FAE姓名', style_heading)
    sheet.write(0,1,'区域 ', style_heading)
    sheet.write(0,2,'销售', style_heading)
    sheet.write(0,3,'客户名称', style_heading)
    sheet.write(0,4,'客户分类', style_heading)
    sheet.write(0,5,'事件名称', style_heading)
    sheet.write(0,6,'发起时间', style_heading)
    sheet.write(0,7,'要求回复时间', style_heading)
    sheet.write(0,8,'预计用时   ', style_heading)
    sheet.write(0,9,'过程描述', style_heading)
    sheet.write(0,10,'结束时间', style_heading)
    sheet.write(0,11,'用时估算', style_heading)
    sheet.write(0,12,'是否有问题', style_heading)
    sheet.write(0,13,'问题描述', style_heading)
    sheet.write(0,14,'满意度评分', style_heading)
    sheet.write(0,15,'评价', style_heading)
    sheet.write(0,16,'成交时间', style_heading)
    sheet.write(0,17,'客户满意度', style_heading)

    #写数据
    form_id = request.session.get('user_id')
    form_user = request.session.get('user_name')
    if request.method == "POST":
        show_name = request.POST.get('show_name')
        # request.session['upshow_name'] = show_name
        show_area = request.POST.get('show_area')
        # request.session['upshow_area'] = show_area
        show_sellname = request.POST.get('show_sellname')
        # request.session['upshow_sellname'] = show_sellname
        showtimestart = request.POST.get('show_timeplan')
        # request.session['upshowtimestart'] = showtimestart
        showtimeend = request.POST.get('show_timeevent')
        # request.session['upshowtimeend'] = showtimeend
        # print(show_name)
        search_dict =dict()
        if show_name :
            search_dict['fae_name__contains'] = show_name
        if show_area :
            search_dict['area__contains'] = show_area
        if show_sellname :
            search_dict['sellname__contains'] = show_sellname
        if request.session.get('user_name') == "陈武" :
            if showtimestart != '' and showtimeend != '':
                find_forminfoevent = FormInfoEvent.objects.filter(**search_dict).filter(start_date__range=(showtimestart,showtimeend)).filter(username__department__contains='技术部').order_by("id")
            if showtimestart == '' or showtimeend == '':
                find_forminfoevent = FormInfoEvent.objects.filter(**search_dict).filter(username__department__contains='技术部').order_by("id")
        if request.session.get('user_name') != "陈武" :
            if showtimestart != '' and showtimeend != '':
                if request.session.get('user_department') == "整机事业部" or request.session.get('user_department') =="渠道事业部":
                    find_forminfoevent = FormInfoEvent.objects.filter(Q(username=form_id) | Q(sellname=form_user)).filter(start_date__range=(showtimestart,showtimeend)).order_by("id")
                if request.session.get('user_department') != "整机事业部" and request.session.get('user_department') != "渠道事业部":
                    find_forminfoevent  = FormInfoEvent.objects.filter(username=form_id).filter(start_date__range=(showtimestart,showtimeend)).order_by("id")
            if showtimestart == '' or showtimeend == '':
                if request.session.get('user_department') == "整机事业部" or request.session.get('user_department') =="渠道事业部":
                    find_forminfoevent = FormInfoEvent.objects.filter(Q(username=form_id) | Q(sellname=form_user)).order_by("id")
                if request.session.get('user_department') != "整机事业部" and request.session.get('user_department') != "渠道事业部":
                    find_forminfoevent  = FormInfoEvent.objects.filter(username=form_id).order_by("id")
        row = 1
        for info in find_forminfoevent:
            sheet.write(row,0,info.fae_name,style_body)
            sheet.write(row,1,info.area,style_body)
            sheet.write(row,2,info.sellname,style_body)
            sheet.write(row,3,info.customer_name,style_body)
            sheet.write(row,4,info.customer_classification,style_body)
            sheet.write(row,5,info.project_name,style_body)
            # 调整宽度
            sheet.col(6).width = 3000
            sheet.write(row,6,info.start_date,style_num)
            try:
                replydate = int(info.reply_date)
            except Exception as e:
                # logging.warning(e)
                replydate = info.reply_date
            sheet.write(row,7,replydate,style_body)
            sheet.write(row,8,info.estimated_time,style_body)
            sheet.write(row,9,info.process,style_body)
            # 调整宽度
            sheet.col(10).width = 3000
            sheet.write(row,10,info.end_date,style_num)
            sheet.write(row,11,info.estimate,style_body)
            sheet.write(row,12,info.is_question,style_body)
            sheet.write(row,13,info.question_describe,style_body)
            sheet.write(row,14,info.satisfaction_score,style_body)
            sheet.write(row,15,info.satisfaction,style_body)
            # 调整宽度
            sheet.col(16).width = 3000
            sheet.write(row,16,info.transaction_time,style_num)
            sheet.write(row,17,info.customer_satisfaction,style_body)
            row = row + 1
        #写出到io
        output = BytesIO()
        wb.save(output)
        #重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
        return response
    return render(request, '404.html')

def export_excelevent_question(request):
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    form_id = request.session.get('user_id')
    form_user = request.session.get('user_name')
    try:
        #找到该用户填写的事件表单
        if request.session.get('user_department') != "整机事业部" and request.session.get('user_department') != "渠道事业部":
            find_forminfoevent = FormInfoEvent.objects.filter(username=form_id).filter(is_question="是").order_by("-id")
        if request.session.get('user_name') == "陈武" :
            find_forminfoevent = FormInfoEvent.objects.filter(username__department__contains='技术部').filter(is_question="是").order_by("-id")
        #分页
        paginatorevent = Paginator(find_forminfoevent,20,1)
        pageevent = request.GET.get('page')
        try:
            formsevent = paginatorevent.page(pageevent)
        except PageNotAnInteger:
            formsevent = paginatorevent.page(1)
        except EmptyPage:
            formsevent = paginatorevent.page(paginatorevent.num_pages)
        return render(request, 'eventquestion.html', {'Forminfoevent': formsevent})

    except Exception as e:
        logging.warning(e)
        return HttpResponse("系统有误!")

def export_excelwork(request):
    # 设置HttpResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = "attachment;filename=FaeWork.xls"
    # 新建一个文件
    wb = xlwt.Workbook(encoding='utf-8')
    # 新建一个sheet
    sheet = wb.add_sheet('日常管理')
    # 样式
    style_heading = xlwt.easyxf("""
        font:
            name 宋体,
            color-index red,
            bold on;
        """
        )
    style_body = xlwt.easyxf("""
        font:
            name 宋体;
        """
        )
    style_num = xlwt.easyxf("""
        font:
            name 宋体;
    """
        )
    style_num.num_format_str = 'yyyy/m/d'

    # 写标题栏
    sheet.write(0,0,'FAE姓名', style_heading)
    sheet.write(0,1,'区域 ', style_heading)
    sheet.write(0,2,'需求者姓名', style_heading)
    sheet.write(0,3,'需求部门', style_heading)
    sheet.write(0,4,'客户名称', style_heading)
    sheet.write(0,5,'事物分类', style_heading)
    sheet.write(0,6,'发起时间', style_heading)
    sheet.write(0,7,'预计用时   ', style_heading)
    sheet.write(0,8,'过程描述', style_heading)
    sheet.write(0,9,'结束时间', style_heading)
    sheet.write(0,10,'用时估算', style_heading)
    sheet.write(0,11,'是否有问题', style_heading)
    sheet.write(0,12,'问题描述', style_heading)
    sheet.write(0,13,'满意度评分', style_heading)
    sheet.write(0,14,'评价', style_heading)
    sheet.write(0,15,'成交时间', style_heading)

    #写数据
    form_id = request.session.get('user_id')
    form_user = request.session.get('user_name')
    if request.method == "POST":
        show_name = request.POST.get('show_name')
        # request.session['upshow_name'] = show_name
        show_area = request.POST.get('show_area')
        # request.session['upshow_area'] = show_area
        show_sellname = request.POST.get('show_sellname')
        # request.session['upshow_sellname'] = show_sellname
        showtimestart = request.POST.get('show_timeplan')
        # request.session['upshowtimestart'] = showtimestart
        showtimeend = request.POST.get('show_timeevent')
        # request.session['upshowtimeend'] = showtimeend
        # print(show_name)
        search_dict =dict()
        if show_name :
            search_dict['fae_name__contains'] = show_name
        if show_area :
            search_dict['area__contains'] = show_area
        if show_sellname :
            search_dict['sellname__contains'] = show_sellname
        if request.session.get('user_name') == "陈武" :
            if showtimestart != '' and showtimeend != '':
                find_forminfowork = FormInfoWork.objects.filter(**search_dict).filter(start_date__range=(showtimestart,showtimeend)).filter(username__department__contains='技术部').order_by("id")
            if showtimestart == '' or showtimeend == '':
                find_forminfowork = FormInfoWork.objects.filter(**search_dict).filter(username__department__contains='技术部').order_by("id")
        if request.session.get('user_name') != "陈武" :
            if showtimestart != '' and showtimeend != '':
                if request.session.get('user_department') == "整机事业部" or request.session.get('user_department') =="渠道事业部":
                    find_forminfowork = FormInfoWork.objects.filter(Q(username=form_id) | Q(sellname=form_user)).filter(start_date__range=(showtimestart,showtimeend)).order_by("id")
                if request.session.get('user_department') != "整机事业部" and request.session.get('user_department') != "渠道事业部":
                    find_forminfowork  = FormInfoWork.objects.filter(username=form_id).filter(start_date__range=(showtimestart,showtimeend)).order_by("id")
            if showtimestart == '' or showtimeend == '':
                if request.session.get('user_department') == "整机事业部" or request.session.get('user_department') =="渠道事业部":
                    find_forminfowork = FormInfoWork.objects.filter(Q(username=form_id) | Q(sellname=form_user)).order_by("id")
                if request.session.get('user_department') != "整机事业部" and request.session.get('user_department') != "渠道事业部":
                    find_forminfowork  = FormInfoWork.objects.filter(username=form_id).order_by("id")
        row = 1
        for info in find_forminfowork:
            sheet.write(row,0,info.fae_name,style_body)
            sheet.write(row,1,info.area,style_body)
            sheet.write(row,2,info.sellname,style_body)
            sheet.write(row,3,info.demand,style_body)
            sheet.write(row,4,info.customer_name,style_body)
            sheet.write(row,5,info.customer_classification,style_body)
            # 调整宽度
            sheet.col(6).width = 3000
            sheet.write(row,6,info.start_date,style_num)
            sheet.write(row,7,info.estimated_time,style_body)
            sheet.write(row,8,info.process,style_body)
            # 调整宽度
            sheet.col(9).width = 3000
            sheet.write(row,9,info.end_date,style_num)
            sheet.write(row,10,info.estimate,style_body)
            sheet.write(row,11,info.is_question,style_body)
            sheet.write(row,12,info.question_describe,style_body)
            sheet.write(row,13,info.satisfaction_score,style_body)
            sheet.write(row,14,info.satisfaction,style_body)
            # 调整宽度
            sheet.col(15).width = 3000
            sheet.write(row,15,info.transaction_time,style_num)
            row = row + 1
        #写出到io
        output = BytesIO()
        wb.save(output)
        #重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
        return response
    return render(request, '404.html')


def export_excelwork_question(request):
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    form_id = request.session.get('user_id')
    form_user = request.session.get('user_name')
    try:
        #找到该用户填写的事件表单
        if request.session.get('user_department') != "整机事业部" and request.session.get('user_department') !="渠道事业部":
            find_forminfowork = FormInfoWork.objects.filter(username=form_id).filter(is_question="是").order_by("-id")
        if request.session.get('user_name') == "陈武" :
            find_forminfowork = FormInfoWork.objects.filter(username__department__contains='技术部').filter(is_question="是").order_by("-id")
        #分页
        paginatorwork = Paginator(find_forminfowork,20,1)
        pagework = request.GET.get('page')
        try:
            formswork = paginatorwork.page(pagework)
        except PageNotAnInteger:
            formswork = paginatorwork.page(1)
        except EmptyPage:
            formswork = paginatorwork.page(paginatorwork.num_pages)
        
        return render(request, 'workquestion.html', {'Forminfowork': formswork})

    except Exception as e:
        logging.warning(e)
        return HttpResponse("系统有误!")

def postplan(request):
    if request.method == 'POST':
        f = request.FILES.get('excel')
        if not f:
            return render(request,'excelplan.html',{'message':'请先上传Excel文件'})
        f = request.FILES['excel']
        type_excel = f.name.split('.')[1]
        if 'xls' == type_excel:
            # 从内存中直接读取前端表单上传的excel文件交给xlrd处理
            wb = xlrd.open_workbook(filename=None,file_contents=f.read())
            if wb.sheet_names() != ['方案管理', '事件管理', '日常管理']:
                return render(request,'excelplan.html',{'message':'Excel文件必须包含三张表格,请检查'})
            #获取excel第一个表
            table = wb.sheets()[0]
            #获取excel第二张表
            table2 = wb.sheets()[1]
            #获取excel第三张表
            table3 = wb.sheets()[2]
            #获取第一个表行数
            nrows = table.nrows
            #获取第二个表行数
            nrows2 = table2.nrows
            #获取第三个表行数
            nrows3 = table3.nrows
            # print(nrows)
            #第一行表头一般不需要
            try:
                with transaction.atomic():
                    for j in range(1,nrows):
                        new_info = FormInfoPlan()
                        #获取名称,根据表具体内容调整下标
                        new_info.fae_name = table.row_values(j)[0]
                        new_info.area = table.row_values(j)[1]
                        new_info.sellname = table.row_values(j)[2]
                        new_info.customer_name = table.row_values(j)[3]
                        new_info.number = int(table.row_values(j)[4])
                        new_info.customer_classification = table.row_values(j)[5]
                        new_info.project_name = table.row_values(j)[6]
                        if (table.cell(j,7).ctype == 3):           
                            d = xlrd.xldate_as_tuple(table.row_values(j)[7],0)
                            d_tmp = date(*d[:3]).strftime('%Y-%m-%d')
                            new_info.start_date = d_tmp
                        else:
                            b = table.row_values(j)[7].replace('/','-').replace('.','-')
                            new_info.start_date = b
                        if (table.cell(j,8).ctype == 2):
                            new_info.reply_date = int(table.row_values(j)[8])
                        else:
                            new_info.reply_date = table.row_values(j)[8]
                        new_info.estimated_time = int(table.row_values(j)[9])
                        new_info.process = table.row_values(j)[10]
                        if (table.cell(j,11).ctype == 3): 
                            d1 = xlrd.xldate_as_tuple(table.row_values(j)[11],0)
                            d1_tmp = date(*d1[:3]).strftime('%Y-%m-%d')
                            new_info.end_date = d1_tmp
                        else:
                            a = table.row_values(j)[11].replace('/','-').replace('.','-')
                            new_info.end_date = a
                        new_info.estimate = int(table.row_values(j)[12])
                        new_info.username = UserInfo.objects.get(id=request.session.get('user_id'))
                        new_info.save()

                    for j in range(1,nrows2):
                        new_info = FormInfoEvent()
                        #获取名称,根据表具体内容调整下标
                        new_info.fae_name = table2.row_values(j)[0]
                        new_info.area = table2.row_values(j)[1]
                        new_info.sellname = table2.row_values(j)[2]
                        new_info.customer_name = table2.row_values(j)[3]
                        # new_info.number = int(table.row_values(j)[4])
                        new_info.customer_classification = table2.row_values(j)[4]
                        new_info.project_name = table2.row_values(j)[5]
                        if (table2.cell(j,6).ctype == 3):           
                            d = xlrd.xldate_as_tuple(table2.row_values(j)[6],0)
                            d_tmp = date(*d[:3]).strftime('%Y-%m-%d')
                            new_info.start_date = d_tmp
                            # print('是时间格式')
                        else:
                            b = table2.row_values(j)[6].replace('/','-').replace('.','-')
                            new_info.start_date = b
                            # print('是文本格式')
                        if (table2.cell(j,7).ctype == 2):
                            new_info.reply_date = int(table2.row_values(j)[7])
                            # print('是数字格式')
                        else:
                            new_info.reply_date = table2.row_values(j)[7]
                            # print('是文本格式')
                        new_info.estimated_time = int(table2.row_values(j)[8])
                        new_info.process = table2.row_values(j)[9]
                        if (table2.cell(j,10).ctype == 3): 
                            d1 = xlrd.xldate_as_tuple(table2.row_values(j)[10],0)
                            d1_tmp = date(*d1[:3]).strftime('%Y-%m-%d')
                            new_info.end_date = d1_tmp
                            # print('是时间格式')
                        else:
                            a = table2.row_values(j)[10].replace('/','-').replace('.','-')
                            new_info.end_date = a
                            # print('是文本格式')
                        new_info.estimate = int(table2.row_values(j)[11])
                        new_info.username = UserInfo.objects.get(id=request.session.get('user_id'))
                        new_info.save()

                    for j in range(1,nrows3):
                        new_info = FormInfoWork()
                        #获取名称,根据表具体内容调整下标
                        new_info.fae_name = table3.row_values(j)[0]
                        new_info.area = table3.row_values(j)[1]
                        new_info.sellname = table3.row_values(j)[2]
                        new_info.demand = table3.row_values(j)[3]
                        new_info.customer_name = table3.row_values(j)[4]
                        # new_info.number = int(table.row_values(j)[4])
                        new_info.customer_classification = table3.row_values(j)[5]
                        # new_info.project_name = table.row_values(j)[6]
                        if (table3.cell(j,6).ctype == 3):           
                            d = xlrd.xldate_as_tuple(table3.row_values(j)[6],0)
                            d_tmp = date(*d[:3]).strftime('%Y-%m-%d')
                            new_info.start_date = d_tmp
                            # print('是时间格式')
                        else:
                            b = table3.row_values(j)[6].replace('/','-').replace('.','-')
                            new_info.start_date = b
                            # print('是文本格式')
                        # if (table.cell(j,8).ctype == 2):
                        #     new_info.reply_date = int(table.row_values(j)[8])
                        # else:
                        #     new_info.reply_date = table.row_values(j)[8]
                        new_info.estimated_time = int(table3.row_values(j)[7])
                        new_info.process = table3.row_values(j)[8]
                        if (table3.cell(j,9).ctype == 3): 
                            d1 = xlrd.xldate_as_tuple(table3.row_values(j)[9],0)
                            d1_tmp = date(*d1[:3]).strftime('%Y-%m-%d')
                            new_info.end_date = d1_tmp
                            # print('是时间格式')
                        else:
                            a = table3.row_values(j)[9].replace('/','-').replace('.','-')
                            new_info.end_date = a
                            # print('是文本格式')
                        new_info.estimate = int(table3.row_values(j)[10])
                        new_info.username = UserInfo.objects.get(id=request.session.get('user_id'))
                        new_info.save()

            except Exception as e:
                logging.warning(e)
                return render(request,'excelplan.html', {'message':'导入失败,请仔细检查文件'})
            return render(request,'excelplan.html',{'message':'导入成功,请返回首页查看'})
        return render(request,'excelplan.html',{'message':'请检查是否是Excel文件'})
    return render(request, '404.html')

def postevent(request):
    if request.method == 'POST':
        f = request.FILES.get('excel')
        if not f:
            return render(request,'excelevent.html',{'message':'请先上传Excel文件'})
        f = request.FILES['excel']
        type_excel = f.name.split('.')[1]
        if 'xls' == type_excel:
            # 从内存中直接读取前端表单上传的excel文件交给xlrd处理
            wb = xlrd.open_workbook(filename=None,file_contents=f.read())
            if wb.sheet_names() != ['方案管理', '事件管理', '日常管理']:
                return render(request,'excelevent.html',{'message':'Excel文件必须包含三张表格,请检查'})
            #获取excel第一个表
            table = wb.sheets()[0]
            #获取excel第二张表
            table2 = wb.sheets()[1]
            #获取excel第三张表
            table3 = wb.sheets()[2]
            #获取第一个表行数
            nrows = table.nrows
            #获取第二个表行数
            nrows2 = table2.nrows
            #获取第三个表行数
            nrows3 = table3.nrows
            # print(nrows)
            #第一行表头一般不需要
            try:
                with transaction.atomic():
                    for j in range(1,nrows):
                        new_info = FormInfoPlan()
                        #获取名称,根据表具体内容调整下标
                        new_info.fae_name = table.row_values(j)[0]
                        new_info.area = table.row_values(j)[1]
                        new_info.sellname = table.row_values(j)[2]
                        new_info.customer_name = table.row_values(j)[3]
                        new_info.number = int(table.row_values(j)[4])
                        new_info.customer_classification = table.row_values(j)[5]
                        new_info.project_name = table.row_values(j)[6]
                        if (table.cell(j,7).ctype == 3):           
                            d = xlrd.xldate_as_tuple(table.row_values(j)[7],0)
                            d_tmp = date(*d[:3]).strftime('%Y-%m-%d')
                            new_info.start_date = d_tmp
                        else:
                            b = table.row_values(j)[7].replace('/','-').replace('.','-')
                            new_info.start_date = b
                        if (table.cell(j,8).ctype == 2):
                            new_info.reply_date = int(table.row_values(j)[8])
                        else:
                            new_info.reply_date = table.row_values(j)[8]
                        new_info.estimated_time = int(table.row_values(j)[9])
                        new_info.process = table.row_values(j)[10]
                        if (table.cell(j,11).ctype == 3): 
                            d1 = xlrd.xldate_as_tuple(table.row_values(j)[11],0)
                            d1_tmp = date(*d1[:3]).strftime('%Y-%m-%d')
                            new_info.end_date = d1_tmp
                        else:
                            a = table.row_values(j)[11].replace('/','-').replace('.','-')
                            new_info.end_date = a
                        new_info.estimate = int(table.row_values(j)[12])
                        new_info.username = UserInfo.objects.get(id=request.session.get('user_id'))
                        new_info.save()

                    for j in range(1,nrows2):
                        new_info = FormInfoEvent()
                        #获取名称,根据表具体内容调整下标
                        new_info.fae_name = table2.row_values(j)[0]
                        new_info.area = table2.row_values(j)[1]
                        new_info.sellname = table2.row_values(j)[2]
                        new_info.customer_name = table2.row_values(j)[3]
                        # new_info.number = int(table.row_values(j)[4])
                        new_info.customer_classification = table2.row_values(j)[4]
                        new_info.project_name = table2.row_values(j)[5]
                        if (table2.cell(j,6).ctype == 3):           
                            d = xlrd.xldate_as_tuple(table2.row_values(j)[6],0)
                            d_tmp = date(*d[:3]).strftime('%Y-%m-%d')
                            new_info.start_date = d_tmp
                            # print('是时间格式')
                        else:
                            b = table2.row_values(j)[6].replace('/','-').replace('.','-')
                            new_info.start_date = b
                            # print('是文本格式')
                        if (table2.cell(j,7).ctype == 2):
                            new_info.reply_date = int(table2.row_values(j)[7])
                            # print('是数字格式')
                        else:
                            new_info.reply_date = table2.row_values(j)[7]
                            # print('是文本格式')
                        new_info.estimated_time = int(table2.row_values(j)[8])
                        new_info.process = table2.row_values(j)[9]
                        if (table2.cell(j,10).ctype == 3): 
                            d1 = xlrd.xldate_as_tuple(table2.row_values(j)[10],0)
                            d1_tmp = date(*d1[:3]).strftime('%Y-%m-%d')
                            new_info.end_date = d1_tmp
                            # print('是时间格式')
                        else:
                            a = table2.row_values(j)[10].replace('/','-').replace('.','-')
                            new_info.end_date = a
                            # print('是文本格式')
                        new_info.estimate = int(table2.row_values(j)[11])
                        new_info.username = UserInfo.objects.get(id=request.session.get('user_id'))
                        new_info.save()

                    for j in range(1,nrows3):
                        new_info = FormInfoWork()
                        #获取名称,根据表具体内容调整下标
                        new_info.fae_name = table3.row_values(j)[0]
                        new_info.area = table3.row_values(j)[1]
                        new_info.sellname = table3.row_values(j)[2]
                        new_info.demand = table3.row_values(j)[3]
                        new_info.customer_name = table3.row_values(j)[4]
                        # new_info.number = int(table.row_values(j)[4])
                        new_info.customer_classification = table3.row_values(j)[5]
                        # new_info.project_name = table.row_values(j)[6]
                        if (table3.cell(j,6).ctype == 3):           
                            d = xlrd.xldate_as_tuple(table3.row_values(j)[6],0)
                            d_tmp = date(*d[:3]).strftime('%Y-%m-%d')
                            new_info.start_date = d_tmp
                            # print('是时间格式')
                        else:
                            b = table3.row_values(j)[6].replace('/','-').replace('.','-')
                            new_info.start_date = b
                            # print('是文本格式')
                        # if (table.cell(j,8).ctype == 2):
                        #     new_info.reply_date = int(table.row_values(j)[8])
                        # else:
                        #     new_info.reply_date = table.row_values(j)[8]
                        new_info.estimated_time = int(table3.row_values(j)[7])
                        new_info.process = table3.row_values(j)[8]
                        if (table3.cell(j,9).ctype == 3): 
                            d1 = xlrd.xldate_as_tuple(table3.row_values(j)[9],0)
                            d1_tmp = date(*d1[:3]).strftime('%Y-%m-%d')
                            new_info.end_date = d1_tmp
                            # print('是时间格式')
                        else:
                            a = table3.row_values(j)[9].replace('/','-').replace('.','-')
                            new_info.end_date = a
                            # print('是文本格式')
                        new_info.estimate = int(table3.row_values(j)[10])
                        new_info.username = UserInfo.objects.get(id=request.session.get('user_id'))
                        new_info.save()

            except Exception as e:
                logging.warning(e)
                return render(request,'excelevent.html', {'message':'导入失败,请仔细检查文件'})
            return render(request,'excelevent.html',{'message':'导入成功,请返回首页查看'})
        return render(request,'excelevent.html',{'message':'请检查是否是Excel文件'})
    return render(request, '404.html')

def postwork(request):
    if request.method == 'POST':
        f = request.FILES.get('excel')
        if not f:
            return render(request,'excelwork.html',{'message':'请先上传Excel文件'})
        f = request.FILES['excel']
        type_excel = f.name.split('.')[1]
        if 'xls' == type_excel:
            # 从内存中直接读取前端表单上传的excel文件交给xlrd处理
            wb = xlrd.open_workbook(filename=None,file_contents=f.read())
            if wb.sheet_names() != ['方案管理', '事件管理', '日常管理']:
                return render(request,'excelevent.html',{'message':'Excel文件必须包含三张表格,请检查'})
            #获取excel第一个表
            table = wb.sheets()[0]
            #获取excel第二张表
            table2 = wb.sheets()[1]
            #获取excel第三张表
            table3 = wb.sheets()[2]
            #获取第一个表行数
            nrows = table.nrows
            #获取第二个表行数
            nrows2 = table2.nrows
            #获取第三个表行数
            nrows3 = table3.nrows
            # print(nrows)
            #第一行表头一般不需要
            try:
                with transaction.atomic():
                    for j in range(1,nrows):
                        new_info = FormInfoPlan()
                        #获取名称,根据表具体内容调整下标
                        new_info.fae_name = table.row_values(j)[0]
                        new_info.area = table.row_values(j)[1]
                        new_info.sellname = table.row_values(j)[2]
                        new_info.customer_name = table.row_values(j)[3]
                        new_info.number = int(table.row_values(j)[4])
                        new_info.customer_classification = table.row_values(j)[5]
                        new_info.project_name = table.row_values(j)[6]
                        if (table.cell(j,7).ctype == 3):           
                            d = xlrd.xldate_as_tuple(table.row_values(j)[7],0)
                            d_tmp = date(*d[:3]).strftime('%Y-%m-%d')
                            new_info.start_date = d_tmp
                        else:
                            b = table.row_values(j)[7].replace('/','-').replace('.','-')
                            new_info.start_date = b
                        if (table.cell(j,8).ctype == 2):
                            new_info.reply_date = int(table.row_values(j)[8])
                        else:
                            new_info.reply_date = table.row_values(j)[8]
                        new_info.estimated_time = int(table.row_values(j)[9])
                        new_info.process = table.row_values(j)[10]
                        if (table.cell(j,11).ctype == 3): 
                            d1 = xlrd.xldate_as_tuple(table.row_values(j)[11],0)
                            d1_tmp = date(*d1[:3]).strftime('%Y-%m-%d')
                            new_info.end_date = d1_tmp
                        else:
                            a = table.row_values(j)[11].replace('/','-').replace('.','-')
                            new_info.end_date = a
                        new_info.estimate = int(table.row_values(j)[12])
                        new_info.username = UserInfo.objects.get(id=request.session.get('user_id'))
                        new_info.save()

                    for j in range(1,nrows2):
                        new_info = FormInfoEvent()
                        #获取名称,根据表具体内容调整下标
                        new_info.fae_name = table2.row_values(j)[0]
                        new_info.area = table2.row_values(j)[1]
                        new_info.sellname = table2.row_values(j)[2]
                        new_info.customer_name = table2.row_values(j)[3]
                        # new_info.number = int(table.row_values(j)[4])
                        new_info.customer_classification = table2.row_values(j)[4]
                        new_info.project_name = table2.row_values(j)[5]
                        if (table2.cell(j,6).ctype == 3):           
                            d = xlrd.xldate_as_tuple(table2.row_values(j)[6],0)
                            d_tmp = date(*d[:3]).strftime('%Y-%m-%d')
                            new_info.start_date = d_tmp
                            # print('是时间格式')
                        else:
                            b = table2.row_values(j)[6].replace('/','-').replace('.','-')
                            new_info.start_date = b
                            # print('是文本格式')
                        if (table2.cell(j,7).ctype == 2):
                            new_info.reply_date = int(table2.row_values(j)[7])
                            # print('是数字格式')
                        else:
                            new_info.reply_date = table2.row_values(j)[7]
                            # print('是文本格式')
                        new_info.estimated_time = int(table2.row_values(j)[8])
                        new_info.process = table2.row_values(j)[9]
                        if (table2.cell(j,10).ctype == 3): 
                            d1 = xlrd.xldate_as_tuple(table2.row_values(j)[10],0)
                            d1_tmp = date(*d1[:3]).strftime('%Y-%m-%d')
                            new_info.end_date = d1_tmp
                            # print('是时间格式')
                        else:
                            a = table2.row_values(j)[10].replace('/','-').replace('.','-')
                            new_info.end_date = a
                            # print('是文本格式')
                        new_info.estimate = int(table2.row_values(j)[11])
                        new_info.username = UserInfo.objects.get(id=request.session.get('user_id'))
                        new_info.save()

                    for j in range(1,nrows3):
                        new_info = FormInfoWork()
                        #获取名称,根据表具体内容调整下标
                        new_info.fae_name = table3.row_values(j)[0]
                        new_info.area = table3.row_values(j)[1]
                        new_info.sellname = table3.row_values(j)[2]
                        new_info.demand = table3.row_values(j)[3]
                        new_info.customer_name = table3.row_values(j)[4]
                        # new_info.number = int(table.row_values(j)[4])
                        new_info.customer_classification = table3.row_values(j)[5]
                        # new_info.project_name = table.row_values(j)[6]
                        if (table3.cell(j,6).ctype == 3):           
                            d = xlrd.xldate_as_tuple(table3.row_values(j)[6],0)
                            d_tmp = date(*d[:3]).strftime('%Y-%m-%d')
                            new_info.start_date = d_tmp
                            # print('是时间格式')
                        else:
                            b = table3.row_values(j)[6].replace('/','-').replace('.','-')
                            new_info.start_date = b
                            # print('是文本格式')
                        # if (table.cell(j,8).ctype == 2):
                        #     new_info.reply_date = int(table.row_values(j)[8])
                        # else:
                        #     new_info.reply_date = table.row_values(j)[8]
                        new_info.estimated_time = int(table3.row_values(j)[7])
                        new_info.process = table3.row_values(j)[8]
                        if (table3.cell(j,9).ctype == 3): 
                            d1 = xlrd.xldate_as_tuple(table3.row_values(j)[9],0)
                            d1_tmp = date(*d1[:3]).strftime('%Y-%m-%d')
                            new_info.end_date = d1_tmp
                            # print('是时间格式')
                        else:
                            a = table3.row_values(j)[9].replace('/','-').replace('.','-')
                            new_info.end_date = a
                            # print('是文本格式')
                        new_info.estimate = int(table3.row_values(j)[10])
                        new_info.username = UserInfo.objects.get(id=request.session.get('user_id'))
                        new_info.save()

            except Exception as e:
                logging.warning(e)
                return render(request,'excelwork.html', {'message':'导入失败,请仔细检查文件'})
            return render(request,'excelwork.html',{'message':'导入成功,请返回首页查看'})
        return render(request,'excelwork.html',{'message':'请检查是否是Excel文件'})
    return render(request, '404.html')


def export_excelall(request):
    if not request.session.get('user_name') :
        return render(request, '404.html')
    # 设置HttpResponse的类型
    weekly = int(time.strftime("%W"))
    faename = request.session.get('user_name')
    filename = "FAE管理第%s周%s.xls" %(weekly,faename)
    filename = urlquote(filename)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s'%(filename)
    # 新建一个文件
    wb = xlwt.Workbook(encoding='utf-8')
    # 新建三个sheet
    sheet  = wb.add_sheet('方案管理')
    sheet2 = wb.add_sheet('事件管理')
    sheet3 = wb.add_sheet('日常管理')
    # 样式
    style_heading = xlwt.easyxf("""
        font:
            name 宋体,
            color-index red,
            bold on;
        """
        )
    style_body = xlwt.easyxf("""
        font:
            name 宋体;
        """
        )
    style_num = xlwt.easyxf("""
        font:
            name 宋体;
    """
        )
    style_num.num_format_str = 'yyyy/m/d'

    # 写第一个标题栏
    sheet.write(0,0,'FAE姓名', style_heading)
    sheet.write(0,1,'区域 ', style_heading)
    sheet.write(0,2,'销售', style_heading)
    sheet.write(0,3,'客户名称', style_heading)
    sheet.write(0,4,'数量', style_heading)
    sheet.write(0,5,'客户分类', style_heading)
    sheet.write(0,6,'项目名称', style_heading)
    sheet.write(0,7,'发起时间', style_heading)
    sheet.write(0,8,'要求回复时间', style_heading)
    sheet.write(0,9,'预计用时   ', style_heading)
    sheet.write(0,10,'过程描述', style_heading)
    sheet.write(0,11,'结束时间', style_heading)
    sheet.write(0,12,'用时估算', style_heading)
    sheet.write(0,13,'是否有问题', style_heading)
    sheet.write(0,14,'问题描述', style_heading)
    sheet.write(0,15,'满意度评分', style_heading)
    sheet.write(0,16,'评价', style_heading)
    sheet.write(0,17,'成交时间', style_heading)
    sheet.write(0,18,'客户满意度', style_heading)
    # 写第二个标题栏
    sheet2.write(0,0,'FAE姓名', style_heading)
    sheet2.write(0,1,'区域 ', style_heading)
    sheet2.write(0,2,'销售', style_heading)
    sheet2.write(0,3,'客户名称', style_heading)
    sheet2.write(0,4,'客户分类', style_heading)
    sheet2.write(0,5,'事件名称', style_heading)
    sheet2.write(0,6,'发起时间', style_heading)
    sheet2.write(0,7,'要求回复时间', style_heading)
    sheet2.write(0,8,'预计用时   ', style_heading)
    sheet2.write(0,9,'过程描述', style_heading)
    sheet2.write(0,10,'结束时间', style_heading)
    sheet2.write(0,11,'用时估算', style_heading)
    sheet2.write(0,12,'是否有问题', style_heading)
    sheet2.write(0,13,'问题描述', style_heading)
    sheet2.write(0,14,'满意度评分', style_heading)
    sheet2.write(0,15,'评价', style_heading)
    sheet2.write(0,16,'成交时间', style_heading)
    sheet2.write(0,17,'客户满意度', style_heading)
    #写第三个标题栏
    sheet3.write(0,0,'FAE姓名', style_heading)
    sheet3.write(0,1,'区域 ', style_heading)
    sheet3.write(0,2,'需求者姓名', style_heading)
    sheet3.write(0,3,'需求部门', style_heading)
    sheet3.write(0,4,'客户名称', style_heading)
    sheet3.write(0,5,'事物分类', style_heading)
    sheet3.write(0,6,'发起时间', style_heading)
    sheet3.write(0,7,'预计用时   ', style_heading)
    sheet3.write(0,8,'过程描述', style_heading)
    sheet3.write(0,9,'结束时间', style_heading)
    sheet3.write(0,10,'用时估算', style_heading)
    sheet3.write(0,11,'是否有问题', style_heading)
    sheet3.write(0,12,'问题描述', style_heading)
    sheet3.write(0,13,'满意度评分', style_heading)
    sheet3.write(0,14,'评价', style_heading)
    sheet3.write(0,15,'完成时间', style_heading)

    #写数据
    form_id = request.session.get('user_id')
    # form_user = request.session.get('user_name')
    
    now = datetime.datetime.now()
    last_week_start = now - timedelta(days=now.weekday()+7)
    last_week_end = now - timedelta(days=now.weekday()+1)
    laststart = last_week_start.strftime("%Y-%m-%d")
    lastend = last_week_end.strftime("%Y-%m-%d")

    if request.session.get('user_name') == "陈武" :
        find_forminfoplan = FormInfoPlan.objects.filter(start_date__range=(laststart,lastend)).order_by("id")
        find_forminfoevent = FormInfoEvent.objects.filter(start_date__range=(laststart,lastend)).order_by("id")
        find_forminfowork = FormInfoWork.objects.filter(start_date__range=(laststart,lastend)).order_by("id")
    if request.session.get('user_name') != "陈武" :
        find_forminfoplan  = FormInfoPlan.objects.filter(username=form_id).filter(start_date__range=(laststart,lastend)).order_by("id")
        find_forminfoevent  = FormInfoEvent.objects.filter(username=form_id).filter(start_date__range=(laststart,lastend)).order_by("id")
        find_forminfowork  = FormInfoWork.objects.filter(username=form_id).filter(start_date__range=(laststart,lastend)).order_by("id")
    row = 1
    for info in find_forminfoplan:
        sheet.write(row,0,info.fae_name,style_body)
        sheet.write(row,1,info.area,style_body)
        sheet.write(row,2,info.sellname,style_body)
        sheet.write(row,3,info.customer_name,style_body)
        sheet.write(row,4,info.number,style_body)
        sheet.write(row,5,info.customer_classification,style_body)
        sheet.write(row,6,info.project_name,style_body)
        # 调整宽度
        sheet.col(7).width = 3000
        sheet.write(row,7,info.start_date,style_num)
        try:
            replydate = int(info.reply_date)
        except Exception as e:
            # logging.warning(e)
            replydate = info.reply_date
        sheet.write(row,8,replydate,style_body)
        sheet.write(row,9,info.estimated_time,style_body)
        sheet.write(row,10,info.process,style_body)
        # 调整宽度
        sheet.col(11).width = 3000
        sheet.write(row,11,info.end_date,style_num)
        sheet.write(row,12,info.estimate,style_body)
        sheet.write(row,13,info.is_question,style_body)
        sheet.write(row,14,info.question_describe,style_body)
        sheet.write(row,15,info.satisfaction_score,style_body)
        sheet.write(row,16,info.satisfaction,style_body)
        # 调整宽度
        sheet.col(17).width = 3000
        sheet.write(row,17,info.transaction_time,style_num)
        sheet.write(row,18,info.customer_satisfaction,style_body)
        row = row + 1

    row = 1
    for info in find_forminfoevent:
        sheet2.write(row,0,info.fae_name,style_body)
        sheet2.write(row,1,info.area,style_body)
        sheet2.write(row,2,info.sellname,style_body)
        sheet2.write(row,3,info.customer_name,style_body)
        sheet2.write(row,4,info.customer_classification,style_body)
        sheet2.write(row,5,info.project_name,style_body)
        # 调整宽度
        sheet2.col(6).width = 3000
        sheet2.write(row,6,info.start_date,style_num)
        try:
            replydate = int(info.reply_date)
        except Exception as e:
            # logging.warning(e)
            replydate = info.reply_date
        sheet2.write(row,7,replydate,style_body)
        sheet2.write(row,8,info.estimated_time,style_body)
        sheet2.write(row,9,info.process,style_body)
        # 调整宽度
        sheet2.col(10).width = 3000
        sheet2.write(row,10,info.end_date,style_num)
        sheet2.write(row,11,info.estimate,style_body)
        sheet2.write(row,12,info.is_question,style_body)
        sheet2.write(row,13,info.question_describe,style_body)
        sheet2.write(row,14,info.satisfaction_score,style_body)
        sheet2.write(row,15,info.satisfaction,style_body)
        # 调整宽度
        sheet2.col(16).width = 3000
        sheet2.write(row,16,info.transaction_time,style_num)
        sheet2.write(row,17,info.customer_satisfaction,style_body)
        row = row + 1

    row = 1
    for info in find_forminfowork:
        sheet3.write(row,0,info.fae_name,style_body)
        sheet3.write(row,1,info.area,style_body)
        sheet3.write(row,2,info.sellname,style_body)
        sheet3.write(row,3,info.demand,style_body)
        sheet3.write(row,4,info.customer_name,style_body)
        sheet3.write(row,5,info.customer_classification,style_body)
        # 调整宽度
        sheet3.col(6).width = 3000
        sheet3.write(row,6,info.start_date,style_num)
        sheet3.write(row,7,info.estimated_time,style_body)
        sheet3.write(row,8,info.process,style_body)
        # 调整宽度
        sheet3.col(9).width = 3000
        sheet3.write(row,9,info.end_date,style_num)
        sheet3.write(row,10,info.estimate,style_body)
        sheet3.write(row,11,info.is_question,style_body)
        sheet3.write(row,12,info.question_describe,style_body)
        sheet3.write(row,13,info.satisfaction_score,style_body)
        sheet3.write(row,14,info.satisfaction,style_body)
        # 调整宽度
        sheet3.col(15).width = 3000
        sheet3.write(row,15,info.transaction_time,style_num)
        row = row + 1
    #写出到io
    output = BytesIO()
    wb.save(output)
    #重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response


def export_excelall_(request):
    if not request.session.get('user_name') :
        return render(request, '404.html')
    # 设置HttpResponse的类型
    weekly = int(time.strftime("%W")) + 1
    faename = request.session.get('user_name')
    filename = "FAE管理第%s周%s.xls" %(weekly,faename)
    filename = urlquote(filename)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s'%(filename)
    # 新建一个文件
    wb = xlwt.Workbook(encoding='utf-8')
    # 新建三个sheet
    sheet  = wb.add_sheet('方案管理')
    sheet2 = wb.add_sheet('事件管理')
    sheet3 = wb.add_sheet('日常管理')
    # 样式
    style_heading = xlwt.easyxf("""
        font:
            name 宋体,
            color-index red,
            bold on;
        """
        )
    style_body = xlwt.easyxf("""
        font:
            name 宋体;
        """
        )
    style_num = xlwt.easyxf("""
        font:
            name 宋体;
    """
        )
    style_num.num_format_str = 'yyyy/m/d'

    # 写第一个标题栏
    sheet.write(0,0,'FAE姓名', style_heading)
    sheet.write(0,1,'区域 ', style_heading)
    sheet.write(0,2,'销售', style_heading)
    sheet.write(0,3,'客户名称', style_heading)
    sheet.write(0,4,'数量', style_heading)
    sheet.write(0,5,'客户分类', style_heading)
    sheet.write(0,6,'项目名称', style_heading)
    sheet.write(0,7,'发起时间', style_heading)
    sheet.write(0,8,'要求回复时间', style_heading)
    sheet.write(0,9,'预计用时   ', style_heading)
    sheet.write(0,10,'过程描述', style_heading)
    sheet.write(0,11,'结束时间', style_heading)
    sheet.write(0,12,'用时估算', style_heading)
    sheet.write(0,13,'是否有问题', style_heading)
    sheet.write(0,14,'问题描述', style_heading)
    sheet.write(0,15,'满意度评分', style_heading)
    sheet.write(0,16,'评价', style_heading)
    sheet.write(0,17,'成交时间', style_heading)
    sheet.write(0,18,'客户满意度', style_heading)
    # 写第二个标题栏
    sheet2.write(0,0,'FAE姓名', style_heading)
    sheet2.write(0,1,'区域 ', style_heading)
    sheet2.write(0,2,'销售', style_heading)
    sheet2.write(0,3,'客户名称', style_heading)
    sheet2.write(0,4,'客户分类', style_heading)
    sheet2.write(0,5,'事件名称', style_heading)
    sheet2.write(0,6,'发起时间', style_heading)
    sheet2.write(0,7,'要求回复时间', style_heading)
    sheet2.write(0,8,'预计用时   ', style_heading)
    sheet2.write(0,9,'过程描述', style_heading)
    sheet2.write(0,10,'结束时间', style_heading)
    sheet2.write(0,11,'用时估算', style_heading)
    sheet2.write(0,12,'是否有问题', style_heading)
    sheet2.write(0,13,'问题描述', style_heading)
    sheet2.write(0,14,'满意度评分', style_heading)
    sheet2.write(0,15,'评价', style_heading)
    sheet2.write(0,16,'成交时间', style_heading)
    sheet2.write(0,17,'客户满意度', style_heading)
    #写第三个标题栏
    sheet3.write(0,0,'FAE姓名', style_heading)
    sheet3.write(0,1,'区域 ', style_heading)
    sheet3.write(0,2,'需求者姓名', style_heading)
    sheet3.write(0,3,'需求部门', style_heading)
    sheet3.write(0,4,'客户名称', style_heading)
    sheet3.write(0,5,'事物分类', style_heading)
    sheet3.write(0,6,'发起时间', style_heading)
    sheet3.write(0,7,'预计用时   ', style_heading)
    sheet3.write(0,8,'过程描述', style_heading)
    sheet3.write(0,9,'结束时间', style_heading)
    sheet3.write(0,10,'用时估算', style_heading)
    sheet3.write(0,11,'是否有问题', style_heading)
    sheet3.write(0,12,'问题描述', style_heading)
    sheet3.write(0,13,'满意度评分', style_heading)
    sheet3.write(0,14,'评价', style_heading)
    sheet3.write(0,15,'完成时间', style_heading)

    #写数据
    form_id = request.session.get('user_id')
    # form_user = request.session.get('user_name')
    
    now = datetime.datetime.now()
    this_week_start = now - timedelta(days=now.weekday())
    this_week_end = now + timedelta(days=6-now.weekday())
    thisstart = this_week_start.strftime("%Y-%m-%d")
    thisend = this_week_end.strftime("%Y-%m-%d")

    if request.session.get('user_name') == "陈武" :
        find_forminfoplan = FormInfoPlan.objects.filter(start_date__range=(thisstart,thisend)).order_by("id")
        find_forminfoevent = FormInfoEvent.objects.filter(start_date__range=(thisstart,thisend)).order_by("id")
        find_forminfowork = FormInfoWork.objects.filter(start_date__range=(thisstart,thisend)).order_by("id")
    if request.session.get('user_name') != "陈武" :
        find_forminfoplan  = FormInfoPlan.objects.filter(username=form_id).filter(start_date__range=(thisstart,thisend)).order_by("id")
        find_forminfoevent  = FormInfoEvent.objects.filter(username=form_id).filter(start_date__range=(thisstart,thisend)).order_by("id")
        find_forminfowork  = FormInfoWork.objects.filter(username=form_id).filter(start_date__range=(thisstart,thisend)).order_by("id")
    row = 1
    for info in find_forminfoplan:
        sheet.write(row,0,info.fae_name,style_body)
        sheet.write(row,1,info.area,style_body)
        sheet.write(row,2,info.sellname,style_body)
        sheet.write(row,3,info.customer_name,style_body)
        sheet.write(row,4,info.number,style_body)
        sheet.write(row,5,info.customer_classification,style_body)
        sheet.write(row,6,info.project_name,style_body)
        # 调整宽度
        sheet.col(7).width = 3000
        sheet.write(row,7,info.start_date,style_num)
        try:
            replydate = int(info.reply_date)
        except Exception as e:
            # logging.warning(e)
            replydate = info.reply_date
        sheet.write(row,8,replydate,style_body)
        sheet.write(row,9,info.estimated_time,style_body)
        sheet.write(row,10,info.process,style_body)
        # 调整宽度
        sheet.col(11).width = 3000
        sheet.write(row,11,info.end_date,style_num)
        sheet.write(row,12,info.estimate,style_body)
        sheet.write(row,13,info.is_question,style_body)
        sheet.write(row,14,info.question_describe,style_body)
        sheet.write(row,15,info.satisfaction_score,style_body)
        sheet.write(row,16,info.satisfaction,style_body)
        # 调整宽度
        sheet.col(17).width = 3000
        sheet.write(row,17,info.transaction_time,style_num)
        sheet.write(row,18,info.customer_satisfaction,style_body)
        row = row + 1

    row = 1
    for info in find_forminfoevent:
        sheet2.write(row,0,info.fae_name,style_body)
        sheet2.write(row,1,info.area,style_body)
        sheet2.write(row,2,info.sellname,style_body)
        sheet2.write(row,3,info.customer_name,style_body)
        sheet2.write(row,4,info.customer_classification,style_body)
        sheet2.write(row,5,info.project_name,style_body)
        # 调整宽度
        sheet2.col(6).width = 3000
        sheet2.write(row,6,info.start_date,style_num)
        try:
            replydate = int(info.reply_date)
        except Exception as e:
            # logging.warning(e)
            replydate = info.reply_date
        sheet2.write(row,7,replydate,style_body)
        sheet2.write(row,8,info.estimated_time,style_body)
        sheet2.write(row,9,info.process,style_body)
        # 调整宽度
        sheet2.col(10).width = 3000
        sheet2.write(row,10,info.end_date,style_num)
        sheet2.write(row,11,info.estimate,style_body)
        sheet2.write(row,12,info.is_question,style_body)
        sheet2.write(row,13,info.question_describe,style_body)
        sheet2.write(row,14,info.satisfaction_score,style_body)
        sheet2.write(row,15,info.satisfaction,style_body)
        # 调整宽度
        sheet2.col(16).width = 3000
        sheet2.write(row,16,info.transaction_time,style_num)
        sheet2.write(row,17,info.customer_satisfaction,style_body)
        row = row + 1

    row = 1
    for info in find_forminfowork:
        sheet3.write(row,0,info.fae_name,style_body)
        sheet3.write(row,1,info.area,style_body)
        sheet3.write(row,2,info.sellname,style_body)
        sheet3.write(row,3,info.demand,style_body)
        sheet3.write(row,4,info.customer_name,style_body)
        sheet3.write(row,5,info.customer_classification,style_body)
        # 调整宽度
        sheet3.col(6).width = 3000
        sheet3.write(row,6,info.start_date,style_num)
        sheet3.write(row,7,info.estimated_time,style_body)
        sheet3.write(row,8,info.process,style_body)
        # 调整宽度
        sheet3.col(9).width = 3000
        sheet3.write(row,9,info.end_date,style_num)
        sheet3.write(row,10,info.estimate,style_body)
        sheet3.write(row,11,info.is_question,style_body)
        sheet3.write(row,12,info.question_describe,style_body)
        sheet3.write(row,13,info.satisfaction_score,style_body)
        sheet3.write(row,14,info.satisfaction,style_body)
        # 调整宽度
        sheet3.col(15).width = 3000
        sheet3.write(row,15,info.transaction_time,style_num)
        row = row + 1
    #写出到io
    output = BytesIO()
    wb.save(output)
    #重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response