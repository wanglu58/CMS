# Generated by Django 2.0.8 on 2018-11-28 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellinfo', '0008_auto_20181113_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pipeline',
            name='winrate',
            field=models.FloatField(blank=True, null=True, verbose_name='赢单率'),
        ),
    ]
