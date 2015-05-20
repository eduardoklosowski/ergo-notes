# -*- coding: utf-8 -*-
#
# Copyright 2015 Eduardo Augusto Klosowski
#
# This file is part of Ergo Notes.
#
# Ergo Notes is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ergo Notes is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Ergo Notes.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from .markups import choices_markup, markup_count, markup_function


# Choices

CHOICES_NOTE_MARKUP = [i[:2] for i in choices_markup]

CHOICES_NOTE_PRIORITY = (
    (1, 'Alta'),
    (0, 'Normal'),
    (-1, 'Baixa'),
)


# Models

@python_2_unicode_compatible
class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='usuário', related_name='+')
    priority = models.SmallIntegerField('prioridade', default=0, choices=CHOICES_NOTE_PRIORITY)
    title = models.CharField('título', max_length=32)
    show_on_home = models.BooleanField('mostrar no home', blank=True, default=False)
    create_on = models.DateTimeField('criado em', auto_now_add=True)
    modify_on = models.DateTimeField('atualizado em', auto_now=True)
    markup = models.CharField('markup', max_length=8, default='txt', choices=CHOICES_NOTE_MARKUP)
    text = models.TextField('texto', blank=True)

    class Meta:
        ordering = ('user', '-priority', 'title')
        unique_together = (('user', 'title'),)
        verbose_name = 'nota'
        verbose_name_plural = 'notas'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return ''

    def get_count(self):
        return markup_count[self.markup](self.text)

    def get_show_on_home_display(self):
        if self.show_on_home:
            return 'Sim'
        else:
            return 'Não'

    def get_text_display(self):
        return markup_function[self.markup](self.text)
