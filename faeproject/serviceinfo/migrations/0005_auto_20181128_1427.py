# Generated by Django 2.0.8 on 2018-11-28 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serviceinfo', '0004_auto_20181128_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='客户电话'),
        ),
    ]