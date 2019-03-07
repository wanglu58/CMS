# Generated by Django 2.0.8 on 2018-09-28 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userinfo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormInfoEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fae_name', models.CharField(max_length=10, verbose_name='FAE姓名')),
                ('area', models.CharField(max_length=10, verbose_name='区域')),
                ('sellname', models.CharField(max_length=10, verbose_name='销售')),
                ('customer_name', models.CharField(blank=True, max_length=30, null=None, verbose_name='客户名称')),
                ('customer_classification', models.CharField(blank=True, max_length=30, null=None, verbose_name='客户分类')),
                ('project_name', models.CharField(blank=True, max_length=50, null=None, verbose_name='事件名称')),
                ('start_date', models.DateField(verbose_name='发起时间')),
                ('reply_date', models.CharField(max_length=10, verbose_name='要求回复时间')),
                ('estimated_time', models.CharField(max_length=10, verbose_name='预计用时')),
                ('process', models.TextField(max_length=255, verbose_name='过程描述')),
                ('end_date', models.DateField(verbose_name='结束时间')),
                ('estimate', models.CharField(max_length=10, verbose_name='用时估算')),
                ('is_question', models.CharField(blank=True, max_length=10, null=None, verbose_name='是否有问题')),
                ('question_describe', models.TextField(blank=True, max_length=255, null=None, verbose_name='问题描述')),
                ('satisfaction_score', models.CharField(blank=True, max_length=10, null=None, verbose_name='满意度评分')),
                ('satisfaction', models.CharField(blank=True, max_length=10, null=None, verbose_name='评价')),
                ('transaction_time', models.DateField(blank=True, null=True, verbose_name='成交时间')),
                ('customer_satisfaction', models.CharField(blank=True, max_length=10, null=None, verbose_name='客户满意度')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userinfo.UserInfo', verbose_name='填写人')),
            ],
            options={
                'verbose_name': 'FAE事件管理信息',
                'verbose_name_plural': 'FAE事件管理',
            },
        ),
        migrations.CreateModel(
            name='FormInfoPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fae_name', models.CharField(max_length=10, verbose_name='FAE姓名')),
                ('area', models.CharField(max_length=10, verbose_name='区域')),
                ('sellname', models.CharField(max_length=10, verbose_name='销售')),
                ('customer_name', models.CharField(blank=True, max_length=30, null=None, verbose_name='客户名称')),
                ('number', models.IntegerField(verbose_name='数量')),
                ('customer_classification', models.CharField(blank=True, max_length=30, null=None, verbose_name='客户分类')),
                ('project_name', models.CharField(blank=True, max_length=50, null=None, verbose_name='项目名称')),
                ('start_date', models.DateField(verbose_name='发起时间')),
                ('reply_date', models.CharField(max_length=10, verbose_name='要求回复时间')),
                ('estimated_time', models.CharField(max_length=10, verbose_name='预计用时')),
                ('process', models.TextField(max_length=255, verbose_name='过程描述')),
                ('end_date', models.DateField(verbose_name='结束时间')),
                ('estimate', models.CharField(max_length=10, verbose_name='用时估算')),
                ('is_question', models.CharField(blank=True, max_length=10, null=None, verbose_name='是否有问题')),
                ('question_describe', models.TextField(blank=True, max_length=255, null=None, verbose_name='问题描述')),
                ('satisfaction_score', models.CharField(blank=True, max_length=10, null=None, verbose_name='满意度评分')),
                ('satisfaction', models.CharField(blank=True, max_length=10, null=None, verbose_name='评价')),
                ('transaction_time', models.DateField(blank=True, null=True, verbose_name='成交时间')),
                ('customer_satisfaction', models.CharField(blank=True, max_length=10, null=None, verbose_name='客户满意度')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userinfo.UserInfo', verbose_name='填写人')),
            ],
            options={
                'verbose_name': 'FAE方案管理信息',
                'verbose_name_plural': 'FAE方案管理',
            },
        ),
        migrations.CreateModel(
            name='FormInfoWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fae_name', models.CharField(max_length=10, verbose_name='FAE姓名')),
                ('area', models.CharField(max_length=10, verbose_name='区域')),
                ('sellname', models.CharField(max_length=10, verbose_name='姓名')),
                ('demand', models.CharField(max_length=30, verbose_name='需求部门')),
                ('customer_name', models.CharField(blank=True, max_length=30, null=None, verbose_name='客户名称')),
                ('customer_classification', models.CharField(blank=True, max_length=30, null=None, verbose_name='事物分类')),
                ('start_date', models.DateField(verbose_name='发起时间')),
                ('estimated_time', models.CharField(max_length=10, verbose_name='预计用时')),
                ('process', models.TextField(max_length=255, verbose_name='过程描述')),
                ('end_date', models.DateField(verbose_name='结束时间')),
                ('estimate', models.CharField(max_length=10, verbose_name='用时估算')),
                ('is_question', models.CharField(blank=True, max_length=10, null=None, verbose_name='是否有问题')),
                ('question_describe', models.TextField(blank=True, max_length=255, null=None, verbose_name='问题描述')),
                ('satisfaction_score', models.CharField(blank=True, max_length=10, null=None, verbose_name='满意度评分')),
                ('satisfaction', models.CharField(blank=True, max_length=10, null=None, verbose_name='评价')),
                ('transaction_time', models.DateField(blank=True, null=True, verbose_name='完成时间')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userinfo.UserInfo', verbose_name='填写人')),
            ],
            options={
                'verbose_name': 'FAE日常管理信息',
                'verbose_name_plural': 'FAE日常管理',
            },
        ),
    ]