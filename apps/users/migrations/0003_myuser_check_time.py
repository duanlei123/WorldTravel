# Generated by Django 2.1.13 on 2019-10-22 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_emailverifyrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='check_time',
            field=models.DateField(default='1970-01-01', verbose_name='签到时间'),
        ),
    ]
