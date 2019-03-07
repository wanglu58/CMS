# Generated by Django 2.0.8 on 2018-12-26 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0003_userinfo_employeeid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='isdelete',
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='employeeid',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='工号'),
        ),
    ]
