# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import include, url

from . import views


url_list = [
    url(r'^$', views.note_list, name='index'),

    url(r'^note/$', views.note_list, name='note_list'),
    url(r'^note/add/$', views.note_form, name='note_add'),
    url(r'^note/(?P<pk>\d+)/edit/$', views.note_form, name='note_edit'),
    url(r'^note/(?P<pk>\d+)/changeonhome/$', views.note_changehome, name='note_changehome'),
    url(r'^note/(?P<pk>\d+)/delete/$', views.note_delete, name='note_delete'),
    url(r'^note/(?P<pk>\d+)/export/$', views.note_export, name='note_export'),
]

urlpatterns = [
    url('', include(url_list, namespace='ergonotes')),
]
