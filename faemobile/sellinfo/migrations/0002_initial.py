# Generated by Django 2.0.8 on 2018-11-06 08:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userinfo', '0002_auto_20181016_1635'),
    ]

    operations = [
        migrations.CreateModel(
            name='PipeLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filltime', models.DateField(blank=True, null=True, verbose_name='填表时间')),
                ('area', models.CharField(max_length=10, verbose_name='区域')),
                ('sellname', models.CharField(max_length=10, verbose_name='跟进销售')),
                ('customer_name', models.CharField(max_length=30, verbose_name='客户名称')),
                ('customer_classification', models.CharField(blank=True, max_length=30, null=True, verbose_name='客户分类')),
                ('project_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='项目名称')),
                ('advantage', models.TextField(blank=True, max_length=255, null=True, verbose_name='在该项目中的优势')),
                ('keyperson', models.CharField(blank=True, max_length=10, null=True, verbose_name='项目关键人')),
                ('keypersonduties', models.CharField(blank=True, max_length=10, null=True, verbose_name='关键人职务')),
                ('phone', models.CharField(blank=True, max_length=30, null=True, verbose_name='电话')),
                ('firsttime', models.DateField(blank=True, null=True, verbose_name='第一次接触时间')),
                ('demandtype', models.CharField(blank=True, max_length=30, null=True, verbose_name='需求产品型号')),
                ('demandnumber', models.FloatField(blank=True, null=True, verbose_name='需求数量')),
                ('competitor', models.CharField(blank=True, max_length=30, null=True, verbose_name='竞品型号')),
                ('competitoradvantage', models.CharField(blank=True, max_length=100, null=True, verbose_name='竞品优势')),
                ('expected', models.CharField(blank=True, max_length=30, null=True, verbose_name='预计下单时间')),
                ('process', models.TextField(blank=True, max_length=255, null=True, verbose_name='本周跟进内容')),
                ('winrate', models.CharField(blank=True, max_length=10, null=True, verbose_name='赢单率')),
                ('planprocess', models.TextField(blank=True, max_length=255, null=True, verbose_name='下一步跟进计划及需要支持')),
                ('plantime', models.DateField(blank=True, null=True, verbose_name='计划行动时间')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userinfo.UserInfo', verbose_name='填写人')),
            ],
            options={
                'verbose_name': '销售pipeline周报',
                'verbose_name_plural': '销售pipeline周报信息',
            },
        ),
        migrations.CreateModel(
            name='SellInfoWeekly',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sellname', models.CharField(max_length=10, verbose_name='填写人')),
                ('filltime', models.DateField(verbose_name='填表时间')),
                ('salesamount', models.FloatField(verbose_name='本周销售金额')),
                ('grossprofit', models.FloatField(verbose_name='本周毛利金额')),
                ('process', models.TextField(max_length=800, verbose_name='本周主要工作')),
                ('question', models.TextField(max_length=800, verbose_name='存在问题及建议')),
                ('nextprocess', models.TextField(max_length=800, verbose_name='下周工作安排')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userinfo.UserInfo', verbose_name='填表人')),
            ],
            options={
                'verbose_name': '销售工作周报',
                'verbose_name_plural': '销售工作周报信息',
            },
        ),
    ]
