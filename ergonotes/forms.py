# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from ergo.foundation.forms import FoundationForm

from . import models


class NoteForm(forms.ModelForm, FoundationForm):
    class Meta:
        fields = ('title', 'priority', 'show_on_home', 'format_type', 'text')
        model = models.Note

        foundation_column_class = {
            'title': 'small-12',
            'priority': 'small-6 medium-4',
            'show_on_home': 'small-6 medium-4',
            'format_type': 'small-12 medium-4',
            'text': 'small-12',
        }
