# Generated by Django 2.0.8 on 2018-11-07 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellinfo', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pipeline',
            name='uptime',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='更新时间'),
        ),
    ]
