# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.apps import apps
from django.conf import settings
from django.core.urlresolvers import reverse, resolve
from django.http import HttpRequest
from django.test import Client, TestCase

from . import views
from .models import Note


class NoteTest(TestCase):
    def setUp(self):
        User = apps.get_model(settings.AUTH_USER_MODEL)
        user = User(username='admin')
        user.save()
        self.user = user

    def test_create(self):
        note = Note()
        note.user = self.user
        note.priority = 0
        note.title = 'Test'
        note.show_on_home = True
        note.format_type = 'plain'
        note.text = 'test'
        self.assertTrue(hasattr(note, 'create_on'))
        self.assertTrue(hasattr(note, 'modify_on'))

    def test_str(self):
        note = Note(title='test')
        self.assertEqual(str(note), 'test')

    def test_url(self):
        note = Note(pk=1)
        route = resolve(note.get_absolute_url())
        self.assertEqual(route.func, views.note_form)
        self.assertDictEqual(route.kwargs, {'pk': '1'})

    def test_text_display_linebreaks(self):
        note = Note(text='test1\ntest2')
        self.assertEqual(note.get_text_display(), 'test1<br />test2')

    def test_text_display_escape(self):
        note = Note(text='<ok>')
        self.assertEqual(note.get_text_display(), '&lt;ok&gt;')

    def test_text_display_rst_markup(self):
        note = Note(format_type='rst', text='*test*')
        self.assertEqual(note.get_text_display(), '<p><em>test</em></p>')

    def test_text_display_with_invalid_format_type(self):
        note = Note(format_type='invalid', text='test')
        self.assertEqual(note.get_text_display(), 'test')

    def test_get_count_plain(self):
        note = Note(text='- 1\n- 2')
        self.assertIsNone(note.get_count())

    def test_get_count_rst(self):
        note = Note(format_type='rst', text='*test*')
        self.assertIsNone(note.get_count())

    def test_get_count_rst_list(self):
        note = Note(format_type='rst', text='- test1\n- test2')
        self.assertEqual(note.get_count(), 2)


class NotesConfTest(TestCase):
    def setUp(self):
        self.app = apps.get_app_config('ergonotes')

    def test_app_conf(self):
        self.assertTrue(hasattr(self.app, 'ergo_url'))
        self.assertTrue(hasattr(self.app, 'ergo_url_index'))
        self.assertTrue(hasattr(self.app, 'ergo_verbose_name'))

    def test_app_ergo_notifications(self):
        User = apps.get_model(settings.AUTH_USER_MODEL)
        user = User(username='admin')
        user.save()

        note1 = Note(user=user, title='test1')
        note1.save()
        note2 = Note(user=user, title='test2', show_on_home=True, format_type='rst', text='- test1\n- test2')
        note2.save()

        request = HttpRequest()
        request.user = user

        notifications = self.app.ergo_notifications(request)

        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0]['url'], note2.get_absolute_url())
        self.assertIn(note2.title, notifications[0]['title'])
        self.assertEqual(notifications[0]['count'], 2)
        self.assertIn('text', notifications[0])


class NotesViewsTest(TestCase):
    def setUp(self):
        User = apps.get_model(settings.AUTH_USER_MODEL)
        user = User(username='admin')
        user.set_password('password')
        user.save()

        self.client = Client()
        self.client.login(username='admin', password='password')
        self.user = user
        self.note1 = Note.objects.create(user=user, title='Note 1', text='Text of note 1')
        self.note2 = Note.objects.create(user=user, priority=1, title='Note 2', show_on_home=True,
                                         format_type='rst', text='*test*')

    def test_list(self):
        response = self.client.get(reverse('ergonotes:note_list'))
        self.assertEqual(response.status_code, 200)

    def test_form(self):
        response = self.client.get(reverse('ergonotes:note_add'))
        self.assertEqual(response.status_code, 200)

    def test_form_add(self):
        self.assertEqual(Note.objects.all().count(), 2)
        response = self.client.post(reverse('ergonotes:note_add'), {
            'title': 'Test Live',
            'priority': '1',
            'show_on_home': '1',
            'format_type': 'plain',
            'text': 'Text of test live',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Note.objects.all().count(), 3)

    def test_form_edit(self):
        self.assertFalse(Note.objects.get(pk=self.note1.pk).show_on_home)
        response = self.client.post(reverse('ergonotes:note_edit', args=(str(self.note1.pk))), {
            'title': self.note1.title,
            'priority': self.note1.priority,
            'show_on_home': '1',
            'format_type': self.note1.format_type,
            'text': self.note1.text,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Note.objects.get(pk=self.note1.pk).show_on_home)

    def test_changehome(self):
        self.assertFalse(Note.objects.get(pk=self.note1.pk).show_on_home)
        response = self.client.get(reverse('ergonotes:note_changehome', args=(str(self.note1.pk))))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Note.objects.get(pk=self.note1.pk).show_on_home)

    def test_delete(self):
        self.assertEquals(Note.objects.all().count(), 2)
        response = self.client.get(reverse('ergonotes:note_delete', args=(str(self.note1.pk))))
        self.assertEqual(response.status_code, 200)

    def test_delete_confirm(self):
        self.assertEquals(Note.objects.all().count(), 2)
        response = self.client.get(reverse('ergonotes:note_delete', args=(str(self.note1.pk))), {
            'confirm': 'y',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Note.objects.all().count(), 1)

    def test_export(self):
        response = self.client.get(reverse('ergonotes:note_export', args=(str(self.note2.pk))))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-type'], 'text/x-rst')
