# Generated by Django 2.0.8 on 2018-10-22 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forminfo', '0004_auto_20181022_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forminfoevent',
            name='satisfaction_score',
            field=models.CharField(blank=True, max_length=10, null=None, verbose_name='满意度评分'),
        ),
        migrations.AlterField(
            model_name='forminfoplan',
            name='satisfaction_score',
            field=models.CharField(blank=True, max_length=10, null=None, verbose_name='满意度评分'),
        ),
        migrations.AlterField(
            model_name='forminfowork',
            name='satisfaction_score',
            field=models.CharField(blank=True, max_length=10, null=None, verbose_name='满意度评分'),
        ),
    ]
