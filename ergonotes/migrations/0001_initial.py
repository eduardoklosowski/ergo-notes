# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('priority', models.SmallIntegerField(default=0, choices=[(1, 'High'), (0, 'Normal'), (-1, 'Low')], verbose_name='priority')),
                ('title', models.CharField(max_length=32, verbose_name='title')),
                ('show_on_home', models.BooleanField(default=False, verbose_name='show on home')),
                ('create_on', models.DateTimeField(auto_now_add=True, verbose_name='create on')),
                ('modify_on', models.DateTimeField(auto_now=True, verbose_name='modify on')),
                ('format_type', models.CharField(default='plain', max_length=8, choices=[('rst', 'reStructuredText'), ('plain', 'Simple Text')], verbose_name='format')),
                ('text', models.TextField(blank=True, verbose_name='text')),
                ('user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name_plural': 'notes',
                'ordering': ('user', '-priority', 'title'),
                'verbose_name': 'note',
            },
        ),
        migrations.AlterUniqueTogether(
            name='note',
            unique_together=set([('user', 'title')]),
        ),
    ]
