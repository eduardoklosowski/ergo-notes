# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from ergo.foundation.tables import Table


class NoteTable(Table):
    columns = ({'name': _('Priority'),
                'header_class': 'width-6r',
                'value': lambda x: x.get_priority_display()},

               {'name': _('Note'),
                'value': lambda x: x.get_linkdisplay()},

               {'name': _('Show on Home?'),
                'class': 'show-for-medium-up',
                'header_class': 'width-6r',
                'value': lambda x: x.get_show_on_home_linkdisplay()},

               {'name': _('Text'),
                'class': 'show-for-medium-up',
                'value': lambda x: x.get_text_displaybox()},

               {'name': _('Format'),
                'class': 'show-for-large-up',
                'header_class': 'width-6r',
                'value': lambda x: x.get_format_type_display()})
