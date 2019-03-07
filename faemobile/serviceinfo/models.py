from django.db import models
from userinfo.models import UserInfo
from datetime import *
# Create your models here.

class Service(models.Model):
#表单基本信息
    servicename = models.CharField(verbose_name='填表人', max_length=10,null=False, blank=False)
    filltime = models.DateField(verbose_name = '填表时间', null=False, blank=False)
    area = models.CharField(verbose_name='服务区域',max_length=10,null=False,blank=False)
    sellname = models.CharField(verbose_name='销售姓名', max_length=10,null=False, blank=False)
#客户信息
    customer = models.CharField(verbose_name='客户姓名', max_length=30,null=False,blank=False)
    phone = models.CharField(verbose_name='客户电话', max_length=30,null=True,blank=True )
    company = models.CharField(verbose_name='客户单位',max_length=50,null=True,blank=True)
    address = models.CharField(verbose_name='客户地址',max_length=50,null=True,blank=True)
    productname = models.CharField(verbose_name='产品名称',max_length=50,null=True,blank=True)
    productmodel = models.CharField(verbose_name='产品型号',max_length=30,null=True,blank=True)
    productid = models.CharField(verbose_name='产品序列号',max_length=30,null=True,blank=True)
    salestime = models.DateField(verbose_name='销售时间',null=True,blank=True)
#故障
    faultdescription = models.TextField(verbose_name='故障现象描述',max_length=800,null=True,blank=True)
    faultrecord = models.TextField(verbose_name='故障处理记录',max_length=800,null=True,blank=True)
    faultresult = models.TextField(verbose_name='故障处理结果',max_length=800,null=True,blank=True)
    opinion = models.CharField(verbose_name='意见',max_length=10,null=True,blank=True)
    specificopinion = models.TextField(verbose_name='具体意见',max_length=800,null=True,blank=True)
    username = models.ForeignKey(UserInfo, verbose_name='填写人',on_delete=models.CASCADE)
#合作人(目前最多4个)
    assistant1 = models.CharField(verbose_name='合作人1', max_length=10,null=True, blank=True)
    assistant2 = models.CharField(verbose_name='合作人2', max_length=10,null=True, blank=True)
    assistant3 = models.CharField(verbose_name='合作人3', max_length=10,null=True, blank=True)
    assistant4 = models.CharField(verbose_name='合作人4', max_length=10,null=True, blank=True)

    def formdetail_url(self):
        return '/serviceinfo/showinfo/?project_id={}/'.format(self.id)

    def amenddetail_url(self):
        return '/serviceinfo/amendinfo/?project_id={}/'.format(self.id)

    class Meta:
        verbose_name = '售后工作周报'
        verbose_name_plural = '售后工作信息'

    def __str__(self):
        return '售后工作信息'