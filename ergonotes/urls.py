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

from django.conf.urls import include, url

from . import views


url_list = [
    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^list/$', views.NoteListView.as_view(), name='note_list'),
    url(r'^(?P<pk>\d+)/$', views.NoteDetailView.as_view(), name='note'),
    url(r'^add/$', views.NoteCreateView.as_view(), name='note_add'),
    url(r'^(?P<pk>\d+)/edit/$', views.NoteUpdateView.as_view(), name='note_edit'),
    url(r'^(?P<pk>\d+)/delete/$', views.NoteDeleteView.as_view(), name='note_delete'),
    url(r'^(?P<pk>\d+)/changeonhome/$', views.NoteChangeShowOnHomeView.as_view(), name='note_changeonhome'),
    url(r'^(?P<pk>\d+)/export/(?P<format>\w+)/$', views.NoteExportView.as_view(), name='note_export'),
]

urlpatterns = [
    url('', include(url_list, namespace='ergonotes')),
]
