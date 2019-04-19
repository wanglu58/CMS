# Generated by Django 2.0.8 on 2018-11-14 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userinfo', '0002_auto_20181016_1635'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('servicename', models.CharField(max_length=10, verbose_name='填表人')),
                ('filltime', models.DateField(verbose_name='填表时间')),
                ('area', models.CharField(max_length=10, verbose_name='区域')),
                ('sellname', models.CharField(max_length=10, verbose_name='姓名')),
                ('customer', models.CharField(max_length=30, verbose_name='客户姓名')),
                ('phone', models.CharField(blank=True, max_length=30, null=True, verbose_name='客户电话')),
                ('company', models.CharField(blank=True, max_length=50, null=True, verbose_name='客户单位')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='客户地址')),
                ('productname', models.CharField(blank=True, max_length=50, null=True, verbose_name='产品名称')),
                ('productmodel', models.CharField(blank=True, max_length=30, null=True, verbose_name='产品型号')),
                ('productid', models.CharField(blank=True, max_length=30, null=True, verbose_name='产品序列号')),
                ('salestime', models.DateField(blank=True, null=True, verbose_name='销售时间')),
                ('faultdescription', models.TextField(blank=True, max_length=800, null=True, verbose_name='故障现象描述')),
                ('faultrecord', models.TextField(blank=True, max_length=800, null=True, verbose_name='故障处理记录')),
                ('faultresult', models.TextField(blank=True, max_length=800, null=True, verbose_name='故障处理结果')),
                ('opinion', models.CharField(blank=True, max_length=10, null=True, verbose_name='意见')),
                ('specificopinion', models.TextField(blank=True, max_length=800, null=True, verbose_name='具体意见')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userinfo.UserInfo', verbose_name='填写人')),
            ],
            options={
                'verbose_name': '售后工作周报',
                'verbose_name_plural': '售后工作信息',
            },
        ),
    ]
