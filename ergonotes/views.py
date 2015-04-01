# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _

from .forms import NoteForm
from .models import Note, NOTE_FORMAT_TYPE
from .tables import NoteTable


@login_required
def note_list(request):
    return render(request, 'ergohome/pag_list.html', {
        'template': 'ergonotes/base.html',
        'list': NoteTable(data=Note.objects.filter(user=request.user)),
    })


@login_required
def note_form(request, pk=None):
    if pk:
        note = get_object_or_404(Note, user=request.user, pk=pk)
    else:
        note = None
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            instance = form.instance
            instance.user = request.user
            instance.save()
            messages.add_message(request, messages.INFO, _('Note "%(title)s" saved successfully') % {
                'title': instance.title,
            })
            return redirect(instance)
    else:
        form = NoteForm(instance=note)
    return render(request, 'ergonotes/note_form.html', {
        'form': form,
        'note': note,
    })


@login_required
def note_changehome(request, pk):
    note = get_object_or_404(Note, user=request.user, pk=pk)
    note.show_on_home = not note.show_on_home
    note.save()
    return redirect('ergonotes:note_list')


@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, user=request.user, pk=pk)
    if request.GET.get('confirm', '') == 'y':
        note.delete()
        messages.add_message(request, messages.INFO, _('Note "%(title)s" deleted') % {
            'title': note.title,
        })
        return redirect('ergonotes:note_list')
    return render(request, 'ergohome/pag_delete.html', {
        'template': 'ergonotes/base.html',
        'title': _('Delete note "%(title)s"?') % {'title': note.title}
    })


@login_required
def note_export(request, pk):
    note = get_object_or_404(Note, user=request.user, pk=pk)
    NOTE_FORMAT_TYPE[note.format_type]['mimetype']
    response = HttpResponse(note.text, content_type=NOTE_FORMAT_TYPE[note.format_type]['mimetype'])
    response['Content-Disposition'] = 'attachment; filename="%s.%s"' % (
        note.title,
        NOTE_FORMAT_TYPE[note.format_type]['extension'],
    )
    return response
