# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin

from . import models


@admin.register(models.Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'priority', 'title', 'show_on_home', 'create_on', 'modify_on', 'format_type', 'get_count')
    list_display_links = ('title',)
    list_filter = ('priority', 'format_type')
    search_fields = ('=user', 'title', 'text')
