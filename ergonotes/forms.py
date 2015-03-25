# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms

from . import models


class NoteForm(forms.ModelForm):
    class Meta:
        fields = ('title', 'priority', 'show_on_home', 'format_type', 'text')
        model = models.Note
