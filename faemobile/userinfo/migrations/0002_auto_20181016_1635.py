# Generated by Django 2.0.8 on 2018-10-16 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='isactive',
            field=models.BooleanField(default=False, verbose_name='是否激活此用户'),
        ),
    ]