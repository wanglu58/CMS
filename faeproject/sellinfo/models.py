from django.db import models
from userinfo.models import UserInfo
from datetime import *
# Create your models here.

class SellInfoWeekly(models.Model):
    sellname = models.CharField(verbose_name='填表人', max_length=10,null=False, blank=False)
    filltime = models.DateField(verbose_name = '填表时间', null=False, blank=False)
    salesamount = models.FloatField(verbose_name= '本周销售金额', null=False, blank=False)
    grossprofit = models.FloatField(verbose_name= '本周毛利金额', null=False, blank=False)
    process = models.TextField(verbose_name='本周主要工作', max_length=800, null=False, blank=False)
    question = models.TextField(verbose_name='存在问题及建议',max_length=800,null=False,blank=False)
    nextprocess = models.TextField(verbose_name='下周工作安排',max_length=800,null=False,blank=False)
    username = models.ForeignKey(UserInfo, verbose_name='填写人',on_delete=models.CASCADE)

    def formdetail_url(self):
        return '/sellinfo/showinfo/?project_id={}/'.format(self.id)

    def amenddetail_url(self):
        return '/sellinfo/amendinfo/?project_id={}/'.format(self.id)

    class Meta:
        verbose_name = '销售工作周报'
        verbose_name_plural = '销售工作周报信息'

    def __str__(self):
        return '销售工作周报信息'


class PipeLine(models.Model):
    filltime = models.DateField(verbose_name = '更新时间', null=True, blank=True)
    area = models.CharField(verbose_name='区域',max_length=10,null=False,blank=False)
    sellname = models.CharField(verbose_name='跟进销售', max_length=10,null=False, blank=False)
    customer_name = models.CharField(verbose_name='客户名称', max_length=30, null=False, blank=False)
    customer_classification = models.CharField(verbose_name='客户分类', max_length=30, null=True, blank=True)
    project_name = models.CharField(verbose_name='项目名称', max_length=50, null=True, blank=True)
    advantage = models.TextField(verbose_name='在该项目中的优势',max_length=255,null=True,blank=True)
    keyperson = models.CharField(verbose_name='项目关键人',max_length=10,null=True,blank=True)
    keypersonduties = models.CharField(verbose_name='关键人职务',max_length=10,null=True,blank=True)
    phone = models.CharField(verbose_name='电话', max_length=30,null=True,blank=True )
    firsttime = models.DateField(verbose_name='第一次接触时间',null=True,blank=True)
    demandtype = models.CharField(verbose_name='需求产品型号', max_length=30, null=True,blank=True)
    demandnumber = models.FloatField(verbose_name='需求数量',null=True,blank=True)
    competitor = models.CharField(verbose_name='竞品型号', max_length=30,null=True,blank=True)
    competitoradvantage = models.TextField(verbose_name='竞品优势', max_length=255,null=True,blank=True)
    expected =  models.CharField(verbose_name='预计下单时间', max_length=30,null=True,blank=True)
    process = models.TextField(verbose_name='本周跟进内容',max_length=255,null=True,blank=True)
    # uptime = models.CharField(verbose_name='更新时间',max_length=10,null=True,blank=True)
    winrate = models.FloatField(verbose_name='赢单率',null=True,blank=True)
    planprocess = models.TextField(verbose_name='下一步跟进计划及需要支持',max_length=255,null=True,blank=True)
    plantime = models.DateField(verbose_name='计划行动时间',null=True,blank=True)
    username = models.ForeignKey(UserInfo, verbose_name='填写人',on_delete=models.CASCADE)

    def formdetail_url(self):
        return '/sellinfo/showpipeline/?project_id={}/'.format(self.id)

    def amenddetail_url(self):
        return '/sellinfo/amendinfopipe/?project_id={}/'.format(self.id)

    class Meta:
        verbose_name = '销售pipeline周报'
        verbose_name_plural = '销售pipeline周报信息'

    def __str__(self):
        return '销售pipeline周报信息'

