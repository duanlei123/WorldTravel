# Generated by Django 2.1.13 on 2019-10-18 16:37

import DjangoUeditor.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='标题')),
                ('content', DjangoUeditor.models.UEditorField(default='', verbose_name='内容')),
                ('image', models.ImageField(upload_to='news/%Y/%m', verbose_name='缩略图')),
                ('checknum', models.IntegerField(default=0, verbose_name='查看数')),
                ('classification', models.CharField(choices=[('hot', '热点'), ('active', '活动'), ('culture', '文化'), ('food', '美食'), ('life', '生活'), ('specialty', '特产')], default='hot', max_length=10, verbose_name='资讯分类')),
                ('add_times', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '新闻信息',
                'verbose_name_plural': '新闻信息',
            },
        ),
    ]
