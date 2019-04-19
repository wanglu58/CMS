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

def service(request):
    #售后首页
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    form_id = request.session.get('user_id')
    form_user = request.session.get('user_name')
    form_department = request.session.get('user_department')
    #找到该用户填写的售后单
    if form_department == "科技制造部" :
        find_service = Service.objects.filter(Q(username=form_id)\
         | Q(assistant1=form_user) | Q(assistant2=form_user) | Q(assistant3=form_user)| Q(assistant4=form_user)).order_by("-id")
    if form_user == "庄嘉" :
        find_service = Service.objects.filter(username__city__contains='南京').filter(username__department__contains='科技制造部').order_by("-id")
    # 分页
    paginatorweek = Paginator(find_service,20,1)
    pageweek = request.GET.get('page')
    try:
        formsweek = paginatorweek.page(pageweek)
    except  PageNotAnInteger:
        formsweek = paginatorweek.page(1)
    except EmptyPage:
        formsweek = paginatorweek.page(paginatorweek.num_pages)
    if request.method == "POST" :
        if form_user != "庄嘉" :
            if request.POST.get('show_timestart') !='' and request.POST.get('show_timeend') != '':
                showtimestart = request.POST.get('show_timestart')
                showtimeend = request.POST.get('show_timeend')
            # 找到所有该时间段用户填写的售后单
                find_service = Service.objects.filter(Q(username=form_id)| Q(assistant1=form_user) | Q(assistant2=form_user) \
                    | Q(assistant3=form_user)| Q(assistant4=form_user)).filter(filltime__range=(showtimestart,showtimeend)).order_by("-id")
                return render(request,'service.html',{'serviceinfo':find_service})
            return render(request,'service.html',{'serviceinfo':formsweek})
        show_name = request.POST.get('show_name')
        show_area = request.POST.get('show_area')
        show_sellname = request.POST.get('show_sellname')
        show_customer = request.POST.get('show_customer')
        showtimestart = request.POST.get('show_timestart')
        showtimeend = request.POST.get('show_timeend')
        search_dict = dict()
        if show_name :
            search_dict['servicename__contains'] = show_name
        if show_area :
            search_dict['area__contains'] = show_area
        if show_sellname :
            search_dict['sellname__contains'] = show_sellname
        if show_customer :
            search_dict['customer__contains'] = show_customer
        if showtimestart !='' and showtimeend != '':
            find_service = Service.objects.filter(username__city__contains='南京').filter(username__department__contains='科技制造部')\
            .filter(**search_dict).filter(filltime__range=(showtimestart,showtimeend)).order_by("-id")
        if showtimestart == '' or showtimeend == '':
            find_service = Service.objects.filter(username__city__contains='南京').filter(username__department__contains='科技制造部')\
            .filter(**search_dict).order_by("-id")

        return render(request,'service.html',{'serviceinfo':find_service})


    return render(request,'service.html',{'serviceinfo':formsweek})


def addservice(request):
    #添加跳转
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    return render(request,'addservice.html')

def addservicepost(request):
    #添加service
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        if request.method == "POST":
            new_info = Service()
            times1 = request.POST.get('salestime')
            if times1 == '':
                times1 = None
            new_info.servicename = request.POST.get('servicename')
            new_info.filltime = request.POST.get('filltime')
            new_info.area = request.POST.get('area')
            new_info.sellname = request.POST.get('sellname')
            new_info.customer = request.POST.get('customer')
            new_info.phone = request.POST.get('phone')
            new_info.company = request.POST.get('company')
            new_info.address = request.POST.get('address')
            new_info.productname = request.POST.get('productname')
            new_info.productmodel = request.POST.get('productmodel')
            new_info.productid = request.POST.get('productid')
            new_info.salestime = times1
            new_info.faultdescription = request.POST.get('faultdescription')
            new_info.faultrecord = request.POST.get('faultrecord')
            new_info.faultresult = request.POST.get('faultresult')
            new_info.opinion = request.POST.get('opinion')
            new_info.specificopinion = request.POST.get('specificopinion')
            new_info.assistant1 = request.POST.get('assistant1')
            new_info.assistant2 = request.POST.get('assistant2')
            new_info.assistant3 = request.POST.get('assistant3')
            new_info.assistant4 = request.POST.get('assistant4')
            new_info.username = UserInfo.objects.get(id=request.session.get('user_id'))
            try:
                new_info.save()
            except Exception as e:
                logging.warning(e)
                return HttpResponse("输入格式有误!")
            return HttpResponseRedirect('/serviceinfo/service')
        else:
            return HttpResponse("/serviceinfo/service")


def showinfo(request):
    #查看服务单
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        project_id = request.GET.get('project_id')[:-1]
        form_detailone = Service.objects.filter(id=project_id)
        return render(request,'showservice.html',{'form_detailone':form_detailone})

def amendservice(request):
    #修改售后首页
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        if request.session.get('user_department') == "科技制造部":
            form_id = request.session.get('user_id')
            form_user = request.session.get('user_name')
            find_service = Service.objects.filter(Q(username=form_id)\
                | Q(assistant1=form_user) | Q(assistant2=form_user) | Q(assistant3=form_user)| Q(assistant4=form_user)).order_by("-id")
            #分页
            paginatorweek = Paginator(find_service,20,1)
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
                    find_service = Service.objects.filter(Q(username=form_id)| Q(assistant1=form_user) | Q(assistant2=form_user)\
                     | Q(assistant3=form_user)| Q(assistant4=form_user)).filter(filltime__range=(showtimestart,showtimeend)).order_by("-id")
                    return render(request,'amendservice.html',{'serviceinfo':find_service})
            return render(request,'amendservice.html',{'serviceinfo':formsweek})
        return render(request, 'amendservice.html' ,{'cannotfind':'您目前无权利修改！'})

def amendinfo(request):
    #修改售后展示
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        project_id = request.GET.get('project_id')[:-1]
        form_detailone = Service.objects.filter(id=project_id)
        request.session['form_id'] = project_id
        return render(request,'amendserviceinfo.html',{'form_detailone':form_detailone})

def amendservicepost(request):
    #修改售后
    if not request.session.get('user_name') :
        return render(request, 'unlogin.html', {"message": "先右上角登录再操作!"})
    else:
        if request.method == "POST":
            project_id = request.session.get('form_id')
            update_info = Service.objects.get(id=project_id)
            times1 = request.POST.get('salestime')
            if times1 == '':
                times1 = None
            update_info.servicename = request.POST.get('servicename')
            update_info.filltime = request.POST.get('filltime')
            update_info.area = request.POST.get('area')
            update_info.sellname = request.POST.get('sellname')
            update_info.customer = request.POST.get('customer')
            update_info.phone = request.POST.get('phone')
            update_info.company = request.POST.get('company')
            update_info.address = request.POST.get('address')
            update_info.productname = request.POST.get('productname')
            update_info.productmodel = request.POST.get('productmodel')
            update_info.productid = request.POST.get('productid')
            update_info.salestime = times1
            update_info.faultdescription = request.POST.get('faultdescription')
            update_info.faultrecord = request.POST.get('faultrecord')
            update_info.faultresult = request.POST.get('faultresult')
            update_info.opinion = request.POST.get('opinion')
            update_info.specificopinion = request.POST.get('specificopinion')
            update_info.assistant1 = request.POST.get('assistant1')
            update_info.assistant2 = request.POST.get('assistant2')
            update_info.assistant3 = request.POST.get('assistant3')
            update_info.assistant4 = request.POST.get('assistant4')
            try:
                update_info.save()
            except Exception as e:
                logging.warning(e)
                return HttpResponse("输入格式有误!")
            del request.session['form_id']
            return HttpResponseRedirect('/serviceinfo/amendservice')
        else:
            return HttpResponseRedirect('/serviceinfo/service')


def exportservice(request):
    # 设置HttpResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = "attachment;filename=Service.xls"
    # 设置一个文件
    wb = xlwt.Workbook(encoding='utf-8')
    # 新建一个sheet
    sheet = wb.add_sheet('售后服务单')
    # 样式
    style_heading = xlwt.easyxf("""
        font:
            name 宋体,
            color-index red,
            bold on;
        """
        )
    style_person = xlwt.easyxf("""
        font:
            name 宋体,
            color-index red,
            bold on;
        alignment:
            horz center ;
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
    #写标题栏
    sheet.write(0,0,'填表时间', style_heading)
    sheet.write(0,1,'填表人', style_heading)
    sheet.write(0,2,'服务区域', style_heading)
    sheet.write(0,3,'销售姓名', style_heading)
    sheet.write(0,4,'客户姓名', style_heading)
    sheet.write(0,5,'客户电话', style_heading)
    sheet.write(0,6,'客户单位', style_heading)
    sheet.write(0,7,'客户地址', style_heading)
    sheet.write(0,8,'产品名称', style_heading)
    sheet.write(0,9,'产品型号', style_heading)
    sheet.write(0,10,'产品序列号', style_heading)
    sheet.write(0,11,'销售时间', style_heading)
    sheet.write(0,12,'故障现象描述', style_heading)
    sheet.write(0,13,'故障处理记录', style_heading)
    sheet.write(0,14,'故障处理结果', style_heading)
    sheet.write(0,15,'意见', style_heading)
    sheet.write(0,16,'具体意见', style_heading)
    #合并单元格第0行到第0列的第17列到第20列
    sheet.write_merge(0,0,17,20,'合作人', style_person)

    #写数据
    form_id = request.session.get('user_id')
    form_user = request.session.get('user_name')
    if request.method == "POST":
        show_name = request.POST.get('show_name')
        show_area = request.POST.get('show_area')
        show_sellname = request.POST.get('show_sellname')
        show_customer = request.POST.get('show_customer')
        showtimestart = request.POST.get('show_timestart')
        showtimeend = request.POST.get('show_timeend')
        search_dict = dict()
        if show_name :
            search_dict['servicename__contains'] = show_name
        if show_area :
            search_dict['area__contains'] = show_area
        if show_sellname :
            search_dict['sellname__contains'] = show_sellname
        if show_customer :
            search_dict['customer__contains'] = show_customer
        if request.session.get('user_name') == "庄嘉" :
            if showtimestart != '' and showtimeend != '':
                find_service = Service.objects.filter(username__city__contains='南京').filter(username__department__contains='科技制造部')\
                .filter(**search_dict).filter(filltime__range=(showtimestart,showtimeend)).order_by("-id")
            if showtimestart == '' or showtimeend == '':
                find_service = Service.objects.filter(username__city__contains='南京').filter(username__department__contains='科技制造部')\
                .filter(**search_dict).order_by("-id")
        if request.session.get('user_name') != "庄嘉" :
            if showtimestart == '' or showtimeend == '':
                find_service = Service.objects.filter(Q(username=form_id)| Q(assistant1=form_user) | Q(assistant2=form_user)\
                    | Q(assistant3=form_user)| Q(assistant4=form_user)).order_by("-id")
            if showtimestart != '' and showtimeend != '':
                find_service = Service.objects.filter(Q(username=form_id)| Q(assistant1=form_user) | Q(assistant2=form_user)\
                    | Q(assistant3=form_user)| Q(assistant4=form_user)).filter(filltime__range=(showtimestart,showtimeend)).order_by("-id")
        row = 1
        for info in find_service:
            sheet.col(0).width = 3000
            sheet.write(row,0,info.filltime,style_num)
            sheet.write(row,1,info.servicename,style_body)
            sheet.write(row,2,info.area,style_body)
            sheet.write(row,3,info.sellname,style_body)
            sheet.write(row,4,info.customer,style_body)
            # 调整宽度
            sheet.col(5).width = 3311
            if info.phone != '' :
                number = int(info.phone)
                sheet.write(row,5,number,style_body)
            if info.phone == '' :
                sheet.write(row,5,info.phone,style_body)
            sheet.write(row,6,info.company,style_body)
            sheet.write(row,7,info.address,style_body)
            sheet.write(row,8,info.productname,style_body)
            sheet.write(row,9,info.productmodel,style_body)
            sheet.write(row,10,info.productid,style_body)
            # 调整宽度
            sheet.col(11).width = 3000
            sheet.write(row,11,info.salestime,style_num)
            sheet.write(row,12,info.faultdescription,style_body)
            sheet.write(row,13,info.faultrecord,style_body)
            sheet.write(row,14,info.faultresult,style_body)
            sheet.write(row,15,info.opinion,style_body)
            sheet.write(row,16,info.specificopinion,style_body)
            sheet.write(row,17,info.assistant1,style_body)
            sheet.write(row,18,info.assistant2,style_body)
            sheet.write(row,19,info.assistant3,style_body)
            sheet.write(row,20,info.assistant4,style_body)
            row = row + 1
        # 写出到io
        output = BytesIO()
        wb.save(output)
        # 重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
        return response
    return render(request, '404.html')