# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ErgoNotesConfig(AppConfig):
    name = 'ergonotes'
    verbose_name = _('Ergo Notes')
    ergo_url = 'notes'
    ergo_url_index = 'ergonotes:index'
    ergo_verbose_name = _('Notes')

    def ergo_notifications(self, request):
        html = []
        for note in self.get_model('Note').objects.filter(user=request.user, show_on_home=True):
            html.append({'url': note.get_absolute_url(),
                         'title': _('Note: %(title)s') % {'title': note.title},
                         'count': note.get_count(),
                         'text': note.get_text_display()})
        return html
