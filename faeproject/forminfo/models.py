from django.db import models
from userinfo.models import UserInfo
from datetime import *

# Create your models here.

class FormInfoPlan(models.Model):
    fae_name = models.CharField(verbose_name='FAE姓名', max_length=10, null=False, blank=False)
    area =  models.CharField(verbose_name='区域', max_length=10, null=False, blank=False)
    sellname = models.CharField(verbose_name='销售员姓名', max_length=10,null=False, blank=False)
    customer_name = models.CharField(verbose_name='客户名称', max_length=30, null=None, blank=True)
    number = models.IntegerField(verbose_name='数量',null=False,blank=False)
    customer_classification = models.CharField(verbose_name='客户分类', max_length=30, null=None, blank=True)
    project_name = models.CharField(verbose_name='项目名称', max_length=50, null=None, blank=True)
    start_date = models.DateField(verbose_name='发起时间', null=False, blank=False)
    reply_date = models.CharField(verbose_name='要求回复时间', max_length=10, null=False, blank=False)
    estimated_time = models.IntegerField(verbose_name='预计用时', null=False, blank=False)
    process = models.TextField(verbose_name='过程描述', max_length=255, null=False, blank=False)
    end_date = models.DateField(verbose_name='结束时间', null=False, blank=False)
    estimate = models.IntegerField(verbose_name='用时估算',null=False, blank=False)
    is_question = models.CharField(verbose_name='是否有问题', max_length=10, null=None, blank=True)
    question_describe = models.TextField(verbose_name='问题描述', max_length=255, null=None, blank=True)
    satisfaction_score = models.IntegerField(verbose_name='满意度评分',null=True, blank=True)
    satisfaction = models.CharField(verbose_name='评价',max_length=10,  null=None, blank=True)
    transaction_time = models.DateField(verbose_name='成交时间', null=True, blank=True)
    customer_satisfaction = models.CharField(verbose_name='客户满意度', max_length=10,  null=None, blank=True)
    nums = models.IntegerField(default=0, verbose_name="评论数量",null=False, blank=False)
    username = models.ForeignKey(UserInfo, verbose_name='填写人',on_delete=models.CASCADE)

    def formdetail_url(self):
        return '/forminfo/changeplaninfo/?project_planid={}/'.format(self.id)

    def amenddetail_url(self):
        return '/forminfo/amendplaninfo/?project_planid={}/'.format(self.id)

    def showdetail_url(self):
        return '/forminfo/showplaninfo/?project_id={}/'.format(self.id)

    
    
    class Meta:
        verbose_name = 'FAE方案管理信息'
        verbose_name_plural = 'FAE方案管理'
        

    def __str__(self):
    	return self.fae_name

    

class FormInfoEvent(models.Model):
    fae_name = models.CharField(verbose_name='FAE姓名', max_length=10, null=False, blank=False)
    area =  models.CharField(verbose_name='区域', max_length=10, null=False, blank=False)
    sellname = models.CharField(verbose_name='销售员姓名', max_length=10,null=False, blank=False)
    customer_name = models.CharField(verbose_name='客户名称', max_length=30, null=None, blank=True)
    # number = models.IntegerField(verbose_name='数量',null=False,blank=False)
    customer_classification = models.CharField(verbose_name='客户分类', max_length=30, null=None, blank=True)
    project_name = models.CharField(verbose_name='事件名称', max_length=50, null=None, blank=True)
    start_date = models.DateField(verbose_name='发起时间', null=False, blank=False)
    reply_date = models.CharField(verbose_name='要求回复时间', max_length=10, null=False, blank=False)
    estimated_time = models.IntegerField(verbose_name='预计用时',null=False, blank=False)
    process = models.TextField(verbose_name='过程描述', max_length=255, null=False, blank=False)
    end_date = models.DateField(verbose_name='结束时间', null=False, blank=False)
    estimate = models.IntegerField(verbose_name='用时估算', null=False, blank=False)
    is_question = models.CharField(verbose_name='是否有问题', max_length=10, null=None, blank=True)
    question_describe = models.TextField(verbose_name='问题描述', max_length=255, null=None, blank=True)
    satisfaction_score = models.IntegerField(verbose_name='满意度评分', null=True, blank=True)
    satisfaction = models.CharField(verbose_name='评价',max_length=10,  null=None, blank=True)
    transaction_time = models.DateField(verbose_name='成交时间', null=True, blank=True)
    customer_satisfaction = models.CharField(verbose_name='客户满意度', max_length=10,  null=None, blank=True)
    nums = models.IntegerField(default=0, verbose_name="评论数量",null=False, blank=False)
    username = models.ForeignKey(UserInfo, verbose_name='填写人',on_delete=models.CASCADE)

    def formdetail_url(self):
        return '/forminfo/changeeventinfo/?project_eventid={}/'.format(self.id)

    def amenddetail_url(self):
        return '/forminfo/amendeventinfo/?project_eventid={}/'.format(self.id)

    def showdetail_url(self):
        return '/forminfo/showeventinfo/?project_id={}/'.format(self.id)

    
    class Meta:
        verbose_name = 'FAE事件管理信息'
        verbose_name_plural = 'FAE事件管理'

    def __str__(self):
        return self.fae_name

class FormInfoWork(models.Model):
    fae_name = models.CharField(verbose_name='FAE姓名', max_length=10, null=False, blank=False)
    area =  models.CharField(verbose_name='区域', max_length=10, null=False, blank=False)
    sellname = models.CharField(verbose_name='需求者姓名', max_length=10,null=False, blank=False)
    demand = models.CharField(verbose_name='需求部门', max_length=30,null=False,blank=False)
    customer_name = models.CharField(verbose_name='客户名称', max_length=30, null=None, blank=True)
    # number = models.IntegerField(verbose_name='数量',null=False,blank=False)
    customer_classification = models.CharField(verbose_name='事物分类', max_length=30, null=None, blank=True)
    # project_name = models.CharField(verbose_name='事件名称', max_length=50, null=None, blank=True)
    start_date = models.DateField(verbose_name='发起时间', null=False, blank=False)
    # reply_date = models.CharField(verbose_name='要求回复时间', max_length=10, null=False, blank=False)
    estimated_time = models.IntegerField(verbose_name='预计用时', null=False, blank=False)
    process = models.TextField(verbose_name='过程描述', max_length=255, null=False, blank=False)
    end_date = models.DateField(verbose_name='结束时间', null=False, blank=False)
    estimate = models.IntegerField(verbose_name='用时估算', null=False, blank=False)
    is_question = models.CharField(verbose_name='是否有问题', max_length=10, null=None, blank=True)
    question_describe = models.TextField(verbose_name='问题描述', max_length=255, null=None, blank=True)
    satisfaction_score = models.IntegerField(verbose_name='满意度评分', null=True, blank=True)
    satisfaction = models.CharField(verbose_name='评价',max_length=10,  null=None, blank=True)
    transaction_time = models.DateField(verbose_name='完成时间', null=True, blank=True)
    nums = models.IntegerField(default=0, verbose_name="评论数量",null=False, blank=False)
    # customer_satisfaction = models.CharField(verbose_name='客户满意度', max_length=10,  null=None, blank=True)
    username = models.ForeignKey(UserInfo, verbose_name='填写人',on_delete=models.CASCADE)

    def formdetail_url(self):
        return '/forminfo/changeworkinfo/?project_workid={}/'.format(self.id)

    def amenddetail_url(self):
        return '/forminfo/amendworkinfo/?project_workid={}/'.format(self.id)

    def showdetail_url(self):
        return '/forminfo/showworkinfo/?project_id={}/'.format(self.id)

    

    class Meta:
        verbose_name = 'FAE日常管理信息'
        verbose_name_plural = 'FAE日常管理'

    def __str__(self):
        return self.fae_name

class CommentPlan(models.Model):
    username = models.ForeignKey(UserInfo, verbose_name='评论人',on_delete=models.CASCADE)
    text = models.TextField(verbose_name='评论描述', max_length=255, null=False, blank=False)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    fae_name = models.ForeignKey(FormInfoPlan, verbose_name='被评论人', on_delete=models.CASCADE)

    def deletecomment_url(self):
        return '/forminfo/deleteplancomment/?comment_id={}/'.format(self.id)

    class Meta:
        verbose_name = '方案评论信息'
        verbose_name_plural = '方案评论信息'

    def __str__(self):
        return '评论信息'


class CommentEvent(models.Model):
    username = models.ForeignKey(UserInfo, verbose_name='评论人',on_delete=models.CASCADE)
    text = models.TextField(verbose_name='评论描述', max_length=255, null=False, blank=False)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    fae_name = models.ForeignKey(FormInfoEvent, verbose_name='被评论人',on_delete=models.CASCADE)

    def deletecomment_url(self):
        return '/forminfo/deleteeventcomment/?comment_id={}/'.format(self.id)

    
    class Meta:
        verbose_name = '事件评论信息'
        verbose_name_plural = '事件评论信息'

    def __str__(self):
        return '评论信息'

class CommentWork(models.Model):
    username = models.ForeignKey(UserInfo, verbose_name='评论人',on_delete=models.CASCADE)
    text = models.TextField(verbose_name='评论描述', max_length=255, null=False, blank=False)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    fae_name = models.ForeignKey(FormInfoWork, verbose_name='被评论人',on_delete=models.CASCADE)

    def deletecomment_url(self):
        return '/forminfo/deleteworkcomment/?comment_id={}/'.format(self.id)

    class Meta:
        verbose_name = '日常评论信息'
        verbose_name_plural = '日常评论信息'

    def __str__(self):
        return '评论信息'