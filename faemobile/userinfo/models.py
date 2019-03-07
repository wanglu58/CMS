from django.db import models

# Create your models here.

class UserInfo(models.Model):
    employeeid = models.CharField('工号',max_length=10,null=True,blank=True)
    username = models.CharField('用户名', max_length=40,null=False)
    userpassword = models.CharField('密码',max_length=2555, null=False)
    gender = models.CharField('性别', max_length=10, null=False)
    city = models.CharField('所在城市', max_length=40, null=False)
    department = models.CharField('所属部门', max_length=40, null=False)
    error_number = models.IntegerField('用户密码输错次数', default=0 )
    # isdelete = models.BooleanField('是否删除用户',default=False)
    isactive = models.BooleanField('是否激活此用户',default=False)

    class Meta:
        verbose_name = '用户注册信息'
        verbose_name_plural = '用户注册'

    def __str__(self):
        return self.username