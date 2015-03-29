# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from ergo.foundation.tables import Table


class NoteTable(Table):
    columns = ({'name': _('Priority'),
                'header_class': 'width-6r',
                'value': lambda x: x.get_priority_display()},

               {'name': _('Note'),
                'value': lambda x: mark_safe('<a href="%s">%s</a>' % (
                    x.get_absolute_url(),
                    x.title,
                ))},

               {'name': _('Show on Home?'),
                'class': 'show-for-medium-up',
                'header_class': 'width-6r',
                'value': lambda x: mark_safe('<a href="%s">%s</a>' % (
                    reverse('ergonotes:note_changehome', args=(x.pk,)),
                    _('Yes') if x.show_on_home else _('No'),
                ))},

               {'name': _('Text'),
                'class': 'show-for-medium-up',
                'value': lambda x: x.get_text_display()},

               {'name': _('Format'),
                'class': 'show-for-large-up',
                'header_class': 'width-6r',
                'value': lambda x: x.get_format_type_display()})
