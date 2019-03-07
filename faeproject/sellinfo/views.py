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

# Create your views here.   

def sellweek(request):
    #周报首页
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    form_id = request.session.get('user_id')
    form_user = request.session.get('user_name')
    

    # 找到该用户填写的周报模板
    if request.session.get('user_department') == "整机事业部" or request.session.get('user_department') =="渠道事业部":
        find_sellinfoweekly = SellInfoWeekly.objects.filter(username=form_id).order_by("-id")
    if request.session.get('user_name') == "梅苹华": 
        find_sellinfoweekly = SellInfoWeekly.objects.filter(username__city__contains='南京').filter(username__department__contains='整机事业部').order_by("-id")
    # 分页
    paginatorweek = Paginator(find_sellinfoweekly,20,1)
    pageweek = request.GET.get('page')
    try:
        formsweek = paginatorweek.page(pageweek)
    except  PageNotAnInteger:
        formsweek = paginatorweek.page(1)
    except EmptyPage:
        formsweek = paginatorweek.page(paginatorweek.num_pages)
    if request.method == "POST":
        if request.session.get('user_name') != "梅苹华" :
            if request.POST.get('show_timestart') !='' and request.POST.get('show_timeend') != '':
                showtimestart = request.POST.get('show_timestart')
                showtimeend = request.POST.get('show_timeend')
            # 找到所有该时间段用户填写的方案表单
                if request.session.get('user_department') == "整机事业部" or request.session.get('user_department') =="渠道事业部":
                    find_sellinfoweekly = SellInfoWeekly.objects.filter(username=form_id).filter(filltime__range=(showtimestart,showtimeend)).order_by("-id")
                return render(request,'sellweek.html',{'sellinfoweekly':find_sellinfoweekly})
            return render(request,'sellweek.html',{'sellinfoweekly':formsweek})
        show_name = request.POST.get('show_name')
        showtimestart = request.POST.get('show_timestart')
        showtimeend = request.POST.get('show_timeend')
        search_dict =dict()
        if show_name :
            search_dict['sellname__contains'] = show_name
        if not search_dict:
            if not showtimestart or not showtimeend:
                return render(request,'sellweek.html',{'sellinfoweekly':formsweek})
        if showtimestart !='' and showtimeend != '':
            find_sellinfoweekly = SellInfoWeekly.objects.filter(username__city__contains='南京').filter(username__department__contains='整机事业部')\
            .filter(**search_dict).filter(filltime__range=(showtimestart,showtimeend)).order_by("-id")
        if showtimestart == '' or showtimeend == '':
            find_sellinfoweekly = SellInfoWeekly.objects.filter(username__city__contains='南京').filter(username__department__contains='整机事业部')\
            .filter(**search_dict).order_by("-id")
        return render(request,'sellweek.html',{'sellinfoweekly':find_sellinfoweekly})

    return render(request,'sellweek.html',{'sellinfoweekly':formsweek})

def pipeline(request):
    # 行业周报首页
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    form_id = request.session.get('user_id')
    form_user = request.session.get('user_name')
    # 找到该用户填写的pipeline
    if request.session.get('user_department') == "整机事业部" or request.session.get('user_department') =="渠道事业部":
        find_pipeline = PipeLine.objects.filter(username=form_id).order_by("-id")
    if request.session.get('user_name') == "梅苹华": 
        find_pipeline = PipeLine.objects.filter(username__city__contains='南京').filter(username__department__contains='整机事业部').order_by("-id")
    # 分页
    paginatorweek = Paginator(find_pipeline,20,1)
    pageweek = request.GET.get('page')
    try:
        formsweek = paginatorweek.page(pageweek)
    except  PageNotAnInteger:
        formsweek = paginatorweek.page(1)
    except EmptyPage:
        formsweek = paginatorweek.page(paginatorweek.num_pages)
    if request.method == "POST":
        if request.session.get('user_name') != "梅苹华" :
            if request.POST.get('show_timestart') !='' and request.POST.get('show_timeend') != '':
                showtimestart = request.POST.get('show_timestart')
                showtimeend = request.POST.get('show_timeend')
            # 找到所有该时间段用户填写的方案表单
                if request.session.get('user_department') == "整机事业部" or request.session.get('user_department') =="渠道事业部":
                    find_pipeline = PipeLine.objects.filter(username=form_id).filter(filltime__range=(showtimestart,showtimeend)).order_by("-id")
                return render(request,'pipeline.html',{'pipelineweekly':find_pipeline})
            return render(request,'pipeline.html',{'pipelineweekly':formsweek})
        show_area = request.POST.get('area')
        show_sellname = request.POST.get('sellname')
        show_customer_name = request.POST.get('customer_name')
        showtimestart = request.POST.get('show_timestart')
        showtimeend = request.POST.get('show_timeend')
        search_dict = dict()
        if show_area :
            search_dict['area__contains'] = show_area
        if show_sellname :
            search_dict['sellname__contains'] = show_sellname
        if show_customer_name :
            search_dict['customer_name__contains'] = show_customer_name
        if not search_dict:
            if not showtimestart or not showtimeend:
                return render(request,'pipeline.html',{'pipelineweekly':formsweek})
        if showtimestart !='' and showtimeend != '':
            find_pipeline = PipeLine.objects.filter(username__city__contains='南京').filter(username__department__contains='整机事业部')\
            .filter(**search_dict).filter(filltime__range=(showtimestart,showtimeend)).order_by("-id")
        if showtimestart == '' or showtimeend == '':
            find_pipeline = PipeLine.objects.filter(username__city__contains='南京').filter(username__department__contains='整机事业部')\
            .filter(**search_dict).order_by("-id")
        return render(request,'pipeline.html',{'pipelineweekly':find_pipeline})

    return render(request,'pipeline.html',{'pipelineweekly':formsweek})

def addsellweekly(request):
    #添加跳转
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    return render(request, 'addsellweek.html')

def addpipeline(request):
    #添加跳转
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    return render(request, 'addpipeline.html')


def addsellweek(request):
    #添加周报
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        if request.method == "POST":
            new_info = SellInfoWeekly()
            new_info.sellname = request.POST.get('sellname')
            new_info.filltime = request.POST.get('filltime')
            new_info.salesamount = request.POST.get('salesamount')
            new_info.grossprofit = request.POST.get('grossprofit')
            new_info.process = request.POST.get('process')
            new_info.question = request.POST.get('question')
            new_info.nextprocess = request.POST.get('nextprocess')
            new_info.username = UserInfo.objects.get(id=request.session.get('user_id'))
            try:
                new_info.save()
            except Exception as e:
                logging.warning(e)
                return HttpResponse("输入格式有误!")
            return HttpResponseRedirect('/sellinfo/sellweek')
        else:
            return HttpResponseRedirect('/sellinfo/sellweek')

def addpipelinepost(request):
    #添加pipeline
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        if request.method == "POST":
            new_info = PipeLine()
            times1 = request.POST.get('filltime')
            times2 = request.POST.get('firsttime')
            times3 = request.POST.get('plantime')
            float1 = request.POST.get('demandnumber')
            float2 = request.POST.get('winrate')
            if times1 == '':
                times1 = None
            if times2 == '':
                times2 = None
            if times3 == '':
                times3 = None
            if float1 == '':
                float1 = None
            if float2 == '':
                float2 = None
            else:
                try:
                    float2 = float(float2)/100
                except Exception as e:
                    logging.warning(e)
                    return HttpResponse("输入格式有误!")
            new_info.filltime = times1
            new_info.area = request.POST.get('area')
            new_info.sellname = request.POST.get('sellname')
            new_info.customer_name = request.POST.get('customer_name')
            new_info.customer_classification = request.POST.get('customer_classification')
            new_info.project_name = request.POST.get('project_name')
            new_info.advantage = request.POST.get('advantage')
            new_info.keyperson = request.POST.get('keyperson')
            new_info.keypersonduties = request.POST.get('keypersonduties')
            new_info.phone = request.POST.get('phone')
            new_info.firsttime = times2
            new_info.demandtype = request.POST.get('demandtype')
            new_info.demandnumber = float1
            new_info.competitor = request.POST.get('competitor')
            new_info.competitoradvantage = request.POST.get('competitoradvantage')
            new_info.expected = request.POST.get('expected')
            new_info.process = request.POST.get('process')
            new_info.winrate = float2
            new_info.planprocess = request.POST.get('planprocess')
            new_info.plantime = times3
            new_info.username = UserInfo.objects.get(id=request.session.get('user_id'))
            try :
                new_info.save()
            except Exception as e:
                logging.warning(e)
                return HttpResponse("输入格式有误!")
            return HttpResponseRedirect('/sellinfo/pipeline')
        else:
            return HttpResponseRedirect('/sellinfo/pipeline')

def showinfo(request):
    #查看周报展示
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        project_id = request.GET.get('project_id')[:-1]
        form_detailone = SellInfoWeekly.objects.filter(id=project_id)
        return render(request,'showinfo.html',{'form_detailone':form_detailone})

def showpipeline(request):
    #查看pipeline展示
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        project_id = request.GET.get('project_id')[:-1]
        form_detailone = PipeLine.objects.filter(id=project_id)
        return render(request,'showpipeline.html',{'form_detailone':form_detailone})

def amendsellweek(request):
    #修改周报首页
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        if request.session.get('user_department') == "整机事业部" or request.session.get('user_department') == "渠道事业部":
            form_id = request.session.get('user_id')
            #找到该用户填写的周报
            find_sellinfoweekly = SellInfoWeekly.objects.filter(username=form_id).order_by("-id")
            #分页
            paginatorweek = Paginator(find_sellinfoweekly,20,1)
            pageweek = request.GET.get('page')
            try:
                formsweek = paginatorweek.page(pageweek)
            except  PageNotAnInteger:
                formsweek = paginatorweek.page(1)
            except EmptyPage:
                formsweek = paginatorweek.page(paginatorweek.num_pages)            
            if request.method == "POST":
                if request.POST.get('show_timestart')!= '' and request.POST.get('show_timeend') != '':
                    showtimestart = request.POST.get('show_timestart')
                    showtimeend = request.POST.get('show_timeend')
                    #找到所有该时间段用户填写的周报
                    find_sellinfoweekly = SellInfoWeekly.objects.filter(username=form_id).filter(filltime__range=(showtimestart,showtimeend)).order_by("-id")
                    return render(request,'amendsellweek.html',{'sellinfoweekly':find_sellinfoweekly})
            return render(request,'amendsellweek.html',{'sellinfoweekly':formsweek})
        return render(request, 'amendsellweek.html' ,{'cannotfind':'您目前无权利修改！'})


def amendpipeline(request):
    #修改pipeline首页
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        if request.session.get('user_department') == "整机事业部" or request.session.get('user_department') == "渠道事业部":
            form_id = request.session.get('user_id')
            #找到该用户填写的周报
            find_pipeline = PipeLine.objects.filter(username=form_id).order_by("-id")
            #分页
            paginatorweek = Paginator(find_pipeline,20,1)
            pageweek = request.GET.get('page')
            try:
                formsweek = paginatorweek.page(pageweek)
            except  PageNotAnInteger:
                formsweek = paginatorweek.page(1)
            except EmptyPage:
                formsweek = paginatorweek.page(paginatorweek.num_pages)
            if request.method == "POST":
                if request.POST.get('show_timestart')!= '' and request.POST.get('show_timeend') != '':
                    showtimestart = request.POST.get('show_timestart')
                    showtimeend = request.POST.get('show_timeend')
                    #找到所有该时间段用户填写的pipeline
                    find_pipeline = PipeLine.objects.filter(username=form_id).filter(filltime__range=(showtimestart,showtimeend)).order_by("-id")
                    return render(request,'amendpipeline.html',{'pipelineweekly':find_pipeline})
            return render(request,'amendpipeline.html',{'pipelineweekly':formsweek})
        return render(request, 'amendpipeline.html' ,{'cannotfind':'您目前无权利修改！'})


def amendinfo(request):
    #修改周报展示
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        project_id = request.GET.get('project_id')[:-1]
        form_detailone = SellInfoWeekly.objects.filter(id=project_id)
        request.session['form_id'] = project_id
        return render(request,'amendinfo.html',{'form_detailone':form_detailone})

def amendinfopipe(request):
    #修改pipeline展示
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        project_id = request.GET.get('project_id')[:-1]
        form_detailone = PipeLine.objects.filter(id=project_id)
        request.session['form_id'] = project_id
        return render(request,'amendinfopipe.html',{'form_detailone':form_detailone})

def updateinfo(request):
    # 修改周报
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        if request.method == "POST":
            project_id = request.session.get('form_id')
            update_info = SellInfoWeekly.objects.get(id=project_id)
            update_info.sellname = request.POST.get('sellname')
            update_info.filltime = request.POST.get('filltime')
            update_info.salesamount = request.POST.get('salesamount')
            update_info.grossprofit = request.POST.get('grossprofit')
            update_info.process = request.POST.get('process')
            update_info.question = request.POST.get('question')
            update_info.nextprocess = request.POST.get('nextprocess')           
            try:
                update_info.save()
            except Exception as e:
                logging.warning(e)
                return HttpResponse("输入格式有误!")
            del request.session['form_id']
            return HttpResponseRedirect('/sellinfo/amendsellweek/')
        else:
            return HttpResponseRedirect('/sellinfo/sellweek/')

def updateinfopipe(request):
    # 修改pipeline
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        if request.method == "POST":
            project_id = request.session.get('form_id')
            update_info = PipeLine.objects.get(id=project_id)
            times1 = request.POST.get('filltime')
            times2 = request.POST.get('firsttime')
            times3 = request.POST.get('plantime')
            float1 = request.POST.get('demandnumber')
            float2 = request.POST.get('winrate')
            if times1 == '':
                times1 = None
            if times2 == '':
                times2 = None
            if times3 == '':
                times3 = None
            if float1 == '':
                float1 = None
            if float2 == '':
                float2 = None
            else:
                float2 = float(float2)/100
            update_info.filltime = times1
            update_info.area = request.POST.get('area')
            update_info.sellname = request.POST.get('sellname')
            update_info.customer_name = request.POST.get('customer_name')
            update_info.customer_classification = request.POST.get('customer_classification')
            update_info.project_name = request.POST.get('project_name')
            update_info.advantage = request.POST.get('advantage')
            update_info.keyperson = request.POST.get('keyperson')
            update_info.keypersonduties = request.POST.get('keypersonduties')
            update_info.phone = request.POST.get('phone')
            update_info.firsttime = times2
            update_info.demandtype = request.POST.get('demandtype')
            update_info.demandnumber = float1
            update_info.competitor = request.POST.get('competitor')
            update_info.competitoradvantage = request.POST.get('competitoradvantage')
            update_info.expected = request.POST.get('expected')
            update_info.process = request.POST.get('process')
            update_info.winrate = float2
            update_info.planprocess = request.POST.get('planprocess')
            update_info.plantime = times3
            try:
                update_info.save()
            except Exception as e:
                logging.warning(e)
                return HttpResponse("输入格式有误!")
            del request.session['form_id']
            return HttpResponseRedirect('/sellinfo/amendpipeline/')
        else:
            return HttpResponseRedirect('/sellinfo/pipeline/')

def exportsellweek(request):
    # 设置HttpResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = "attachment;filename=Salesweekly.xls"
    # 新建一个文件
    wb = xlwt.Workbook(encoding='utf-8')
    # 新建一个sheet
    sheet = wb.add_sheet('工作周报')
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
    sheet.write(0,0,'填表人', style_heading)
    sheet.write(0,1,'填表时间 ', style_heading)
    sheet.write(0,2,'本周销售金额', style_heading)
    sheet.write(0,3,'本周毛利金额', style_heading)
    sheet.write(0,4,'本周主要工作', style_heading)
    sheet.write(0,5,'存在问题及建议', style_heading)
    sheet.write(0,6,'下周工作安排', style_heading)

    # 写数据
    form_id = request.session.get('user_id')
    form_user = request.session.get('user_name')
    if request.method == "POST":
        show_name = request.POST.get('show_name')
        showtimestart = request.POST.get('show_timestart')
        showtimeend = request.POST.get('show_timeend')
        search_dict = dict()
        if show_name :
            search_dict['sellname__contains'] = show_name
        if request.session.get('user_name') == "梅苹华" :
            if showtimestart != '' and showtimeend != '':
                find_sellinfoweekly = SellInfoWeekly.objects.filter(username__city__contains='南京').filter(username__department__contains='整机事业部')\
            .filter(**search_dict).filter(filltime__range=(showtimestart,showtimeend)).order_by("-id")
            if showtimestart == '' or showtimeend == '':
                find_sellinfoweekly = SellInfoWeekly.objects.filter(username__city__contains='南京').filter(username__department__contains='整机事业部')\
            .filter(**search_dict).order_by("-id")
        if request.session.get('user_name') != "梅苹华" :
            if showtimestart != '' and showtimeend != '':
                find_sellinfoweekly = SellInfoWeekly.objects.filter(username=form_id).filter(filltime__range=(showtimestart,showtimeend)).order_by("-id")
            if showtimestart == '' or showtimeend == '':
                find_sellinfoweekly = SellInfoWeekly.objects.filter(username=form_id).order_by("-id")
        row = 1
        for info in find_sellinfoweekly:
            # print(info.sellname)
            sheet.write(row,0,info.sellname,style_body)
            # 调整宽度
            sheet.col(1).width = 3000
            sheet.write(row,1,info.filltime,style_num)
            sheet.write(row,2,info.salesamount,style_body)
            sheet.write(row,3,info.grossprofit,style_body)
            sheet.write(row,4,info.process,style_body)
            sheet.write(row,5,info.question,style_body)
            sheet.write(row,6,info.nextprocess,style_body)
            row = row + 1
        # 写出到io
        output = BytesIO()
        wb.save(output)
        # 重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
        return response
    return render(request, '404.html')


def exportpipeline(request):
    # 设置HttpResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = "attachment;filename=Pipelineweekly.xls"
    # 新建一个文件
    wb = xlwt.Workbook(encoding='utf-8')
    # 新建一个sheet
    sheet = wb.add_sheet('行业周报')
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
    style_rate = xlwt.easyxf("""
        font:
            name 宋体;
    """
        )
    style_rate.num_format_str = '0%'
    style_num = xlwt.easyxf("""
        font:
            name 宋体;
    """
        )
    style_num.num_format_str = 'yyyy/m/d'
    #写标题栏
    sheet.write(0,0,'区域', style_heading)
    sheet.write(0,1,'跟进销售', style_heading)
    sheet.write(0,2,'客户名称', style_heading)
    sheet.write(0,3,'客户分类', style_heading)
    sheet.write(0,4,'项目名称', style_heading)
    sheet.write(0,5,'在该项目中的优势', style_heading)
    sheet.write(0,6,'项目关键人', style_heading)
    sheet.write(0,7,'关键人职务', style_heading)
    sheet.write(0,8,'电话号码', style_heading)
    sheet.write(0,9,'首次接触时间', style_heading)
    sheet.write(0,10,'需求产品型号', style_heading)
    sheet.write(0,11,'需求数量(K)', style_heading)
    sheet.write(0,12,'竞品型号', style_heading)
    sheet.write(0,13,'竞品优势', style_heading)
    sheet.write(0,14,'预计下单时间', style_heading)
    sheet.write(0,15,'本周跟进内容', style_heading)
    sheet.write(0,16,'赢单率', style_heading)
    sheet.write(0,17,'更新时间', style_heading)
    sheet.write(0,18,'下一步跟进计划及需要支持', style_heading)
    sheet.write(0,19,'计划行动时间', style_heading)

    #写数据
    form_id = request.session.get('user_id')
    form_user = request.session.get('user_name')
    if request.method == "POST":
        area = request.POST.get('area')
        sellname = request.POST.get('sellname')
        customer_name = request.POST.get('customer_name')
        showtimestart = request.POST.get('show_timestart')
        showtimeend = request.POST.get('show_timeend')
        search_dict = dict()
        if area :
            search_dict['area__contains'] = area
        if sellname :
            search_dict['sellname__contains'] = sellname
        if customer_name :
            search_dict['customer_name__contains'] = customer_name
        if request.session.get('user_name') == "梅苹华" :
            if showtimestart != '' and showtimeend != '':
                find_pipeline = PipeLine.objects.filter(username__city__contains='南京').filter(username__department__contains='整机事业部')\
            .filter(**search_dict).filter(filltime__range=(showtimestart,showtimeend)).order_by("-id")
            if showtimestart == '' or showtimeend == '':
                find_pipeline = PipeLine.objects.filter(username__city__contains='南京').filter(username__department__contains='整机事业部')\
            .filter(**search_dict).order_by("-id")
        if request.session.get('user_name') != "梅苹华" :
            if showtimestart == '' or showtimeend == '':
                find_pipeline = PipeLine.objects.filter(username=form_id).order_by("-id")
            if showtimestart != '' and showtimeend != '':
                find_pipeline = PipeLine.objects.filter(username=form_id).filter(filltime__range=(showtimestart,showtimeend)).order_by("-id")
        row = 1
        for info in find_pipeline:
            sheet.write(row,0,info.area,style_body)
            sheet.write(row,1,info.sellname,style_body)
            sheet.write(row,2,info.customer_name,style_body)
            sheet.write(row,3,info.customer_classification,style_body)
            sheet.write(row,4,info.project_name,style_body)
            sheet.write(row,5,info.advantage,style_body)
            sheet.write(row,6,info.keyperson,style_body)
            sheet.write(row,7,info.keypersonduties,style_body)
            # 调整宽度
            sheet.col(8).width = 3107
            if info.phone != '':
                number = int(info.phone)
                sheet.write(row,8,number,style_body)
            if info.phone == '':
                sheet.write(row,8,info.phone,style_body)
            # 调整宽度
            sheet.col(9).width = 3000
            sheet.write(row,9,info.firsttime,style_num)
            sheet.write(row,10,info.demandtype,style_body)
            sheet.write(row,11,info.demandnumber,style_body)
            sheet.write(row,12,info.competitor,style_body)
            sheet.write(row,13,info.competitoradvantage,style_body)
            sheet.write(row,14,info.expected,style_body)
            sheet.write(row,15,info.process,style_body)
            sheet.write(row,16,info.winrate,style_rate)
            # 调整宽度
            sheet.col(17).width = 3000
            sheet.write(row,17,info.filltime,style_num)
            sheet.write(row,18,info.planprocess,style_body)
            # 调整宽度
            sheet.col(19).width = 3000
            sheet.write(row,19,info.plantime,style_num)
            row = row + 1
        # 写出到io
        output = BytesIO()
        wb.save(output)
        # 重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
        return response
    return render(request, '404.html')