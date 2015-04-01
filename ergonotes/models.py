# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from docutils.core import publish_doctree, publish_parts
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import linebreaksbr
from django.utils.encoding import python_2_unicode_compatible
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


NOTE_FORMAT_TYPE = {
    'plain': {'name': _('Simple Text'), 'extension': 'txt', 'mimetype': 'text/plain'},
    'rst': {'name': _('reStructuredText'), 'extension': 'rst', 'mimetype': 'text/x-rst'},
}


CHOICES_NOTE_FORMAT_TYPE = sorted([(i, _(NOTE_FORMAT_TYPE[i]['name'])) for i in NOTE_FORMAT_TYPE],
                                  key=lambda x: x[1].lower())

CHOICES_NOTE_PRIORITY = (
    (1, _('High')),
    (0, _('Normal')),
    (-1, _('Low')),
)


@python_2_unicode_compatible
class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), related_name='+')
    priority = models.SmallIntegerField(_('priority'), default=0, choices=CHOICES_NOTE_PRIORITY)
    title = models.CharField(_('title'), max_length=32)
    show_on_home = models.BooleanField(_('show on home'), default=False)
    create_on = models.DateTimeField(_('create on'), auto_now_add=True)
    modify_on = models.DateTimeField(_('modify on'), auto_now=True)
    format_type = models.CharField(_('format'), max_length=8, default='plain', choices=CHOICES_NOTE_FORMAT_TYPE)
    text = models.TextField(_('text'), blank=True)

    class Meta:
        ordering = ('user', '-priority', 'title')
        unique_together = (('user', 'title'),)
        verbose_name = _('note')
        verbose_name_plural = _('notes')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ergonotes:note_edit', kwargs={'pk': self.pk})

    def get_linkdisplay(self):
        return mark_safe('<a href="%s">%s</a>' % (self.get_absolute_url(), self.title))

    def get_show_on_home_display(self):
        if self.show_on_home:
            return _('Yes')
        return _('No')

    def get_show_on_home_linkdisplay(self):
        return mark_safe('<a href="%s">%s</a>' % (reverse('ergonotes:note_changehome', args=(self.pk,)),
                                                  self.get_show_on_home_display()))

    def get_text_display(self):
        if self.format_type == 'plain':
            return linebreaksbr(self.text)
        if self.format_type == 'rst':
            parts = publish_parts(self.text, writer_name='html')
            return mark_safe(parts['body'].rstrip())

        return self.text

    def get_text_displaybox(self):
        return mark_safe('<div class="note-box">%s</div>' % self.get_text_display())

    def get_count(self):
        if self.format_type == 'rst':
            tree = publish_doctree(self.text)
            if tree.children[0].tagname == 'bullet_list':
                return len(tree.asdom().getElementsByTagName('list_item'))

        return None
    get_count.short_description = _('notifications')
