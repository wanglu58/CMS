# Generated by Django 2.0.8 on 2018-09-28 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=40, verbose_name='用户名')),
                ('userpassword', models.CharField(max_length=2555, verbose_name='密码')),
                ('gender', models.CharField(max_length=10, verbose_name='性别')),
                ('city', models.CharField(max_length=40, verbose_name='所在城市')),
                ('department', models.CharField(max_length=40, verbose_name='所属部门')),
                ('error_number', models.IntegerField(default=0, verbose_name='用户密码输错次数')),
                ('isdelete', models.BooleanField(default=False, verbose_name='是否删除用户')),
                ('isactive', models.BooleanField(default=True, verbose_name='是否解除封禁')),
            ],
            options={
                'verbose_name': '用户注册信息',
                'verbose_name_plural': '用户注册',
            },
        ),
    ]