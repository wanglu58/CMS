# Generated by Django 2.0.8 on 2018-11-19 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serviceinfo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='area',
            field=models.CharField(max_length=10, verbose_name='服务区域'),
        ),
        migrations.AlterField(
            model_name='service',
            name='sellname',
            field=models.CharField(max_length=10, verbose_name='销售姓名'),
        ),
    ]
