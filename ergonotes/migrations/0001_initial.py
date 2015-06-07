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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('priority', models.SmallIntegerField(choices=[(1, 'Alta'), (0, 'Normal'), (-1, 'Baixa')], default=0, verbose_name='prioridade')),
                ('title', models.CharField(max_length=32, verbose_name='título')),
                ('show_on_home', models.BooleanField(default=False, verbose_name='mostrar no home')),
                ('create_on', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('modify_on', models.DateTimeField(auto_now=True, verbose_name='atualizado em')),
                ('markup', models.CharField(choices=[('txt', 'Texto'), ('html', 'HTML'), ('rst', 'reStructuredText'), ('mk', 'Markdown'), ('textile', 'Textile')], default='txt', verbose_name='markup', max_length=8)),
                ('text', models.TextField(verbose_name='texto', blank=True)),
                ('user', models.ForeignKey(verbose_name='usuário', related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'notas',
                'verbose_name': 'nota',
                'ordering': ('user', '-priority', 'title'),
            },
        ),
        migrations.AlterUniqueTogether(
            name='note',
            unique_together=set([('user', 'title')]),
        ),
    ]
