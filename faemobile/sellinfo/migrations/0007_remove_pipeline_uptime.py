# Generated by Django 2.0.8 on 2018-11-09 01:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sellinfo', '0006_pipeline_uptime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pipeline',
            name='uptime',
        ),
    ]
