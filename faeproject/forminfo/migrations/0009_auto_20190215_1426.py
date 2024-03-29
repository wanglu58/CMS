# Generated by Django 2.0.8 on 2019-02-15 06:26

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0004_auto_20181226_1047'),
        ('forminfo', '0008_auto_20181022_1027'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=255, verbose_name='评论描述')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '事件评论信息',
                'verbose_name_plural': '事件评论信息',
            },
        ),
        migrations.CreateModel(
            name='CommentPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=255, verbose_name='评论描述')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '方案评论信息',
                'verbose_name_plural': '方案评论信息',
            },
        ),
        migrations.CreateModel(
            name='CommentWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=255, verbose_name='评论描述')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '日常评论信息',
                'verbose_name_plural': '日常评论信息',
            },
        ),
        migrations.AddField(
            model_name='forminfoevent',
            name='nums',
            field=models.IntegerField(default=0, verbose_name='评论数量'),
        ),
        migrations.AddField(
            model_name='forminfoplan',
            name='nums',
            field=models.IntegerField(default=0, verbose_name='评论数量'),
        ),
        migrations.AddField(
            model_name='forminfowork',
            name='nums',
            field=models.IntegerField(default=0, verbose_name='评论数量'),
        ),
        migrations.AddField(
            model_name='commentwork',
            name='fae_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forminfo.FormInfoWork', verbose_name='被评论人'),
        ),
        migrations.AddField(
            model_name='commentwork',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userinfo.UserInfo', verbose_name='评论人'),
        ),
        migrations.AddField(
            model_name='commentplan',
            name='fae_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forminfo.FormInfoPlan', verbose_name='被评论人'),
        ),
        migrations.AddField(
            model_name='commentplan',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userinfo.UserInfo', verbose_name='评论人'),
        ),
        migrations.AddField(
            model_name='commentevent',
            name='fae_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forminfo.FormInfoEvent', verbose_name='被评论人'),
        ),
        migrations.AddField(
            model_name='commentevent',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userinfo.UserInfo', verbose_name='评论人'),
        ),
    ]
