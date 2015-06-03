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

from ergo.views import LoginRequiredMixin
from userviews import views as userviews

from . import models


# Note

class NoteListView(LoginRequiredMixin, userviews.UserListView):
    model = models.Note
