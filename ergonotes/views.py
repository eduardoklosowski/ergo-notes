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

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from ergo.views import LoginRequiredMixin
from userviews import views as userviews

from . import models


# Note

class NoteListView(LoginRequiredMixin, userviews.UserListView):
    model = models.Note


class NoteDetailView(LoginRequiredMixin, userviews.UserDetailView):
    model = models.Note


class NoteCreateView(LoginRequiredMixin, userviews.UserCreateView):
    model = models.Note
    fields = ('user', 'priority', 'title', 'show_on_home', 'markup', 'text')


class NoteUpdateView(LoginRequiredMixin, userviews.UserUpdateView):
    model = models.Note
    fields = ('priority', 'title', 'show_on_home', 'markup', 'text')


class NoteDeleteView(LoginRequiredMixin, userviews.UserDeleteView):
    model = models.Note
    success_url = reverse_lazy('ergonotes:note_list')


class NoteChangeShowOnHomeView(LoginRequiredMixin, userviews.UserDetailView):
    model = models.Note

    def get(self, request, *args, **kwargs):
        note = self.get_object()
        note.show_on_home = not note.show_on_home
        note.save()

        url = request.META.get('HTTP_REFERER', note.get_absolute_url())
        return HttpResponseRedirect(url)
