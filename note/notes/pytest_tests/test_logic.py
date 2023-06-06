from http import HTTPStatus

import pytest
from django.urls import reverse, reverse_lazy
from pytest_django.asserts import assertRedirects

from notes.models import Note


def test_user_can_create_note(author_client, author, form):
    url = reverse('notes:create')
    response = author_client.post(url, data=form)
    assertRedirects(response, reverse('notes:list'))
    assert Note.objects.count() == 1
    new_note = Note.objects.get()
    assert new_note.title == form['title']
    assert new_note.text == form['text']
    assert new_note.author == author


@pytest.mark.django_db
def test_anonymous_user_cant_create(client, form):
    url = reverse('notes:create')
    response = client.post(url, data=form)
    login_url = reverse('login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Note.objects.count() == 0


def test_author_can_edit(author_client, author, form, note):
    url = reverse('notes:edit', args=(note.id,))
    response = author_client.post(url, data=form)
    assertRedirects(response, reverse('notes:detail',
                                      args=(note.id,)))
    new_note = Note.objects.get()
    assert new_note.title == form['title']
    assert new_note.text == form['text']
    assert new_note.author == author


def test_other_user_cant_edit_note(admin_client, form, note):
    url = reverse('notes:edit', args=(note.id,))
    response = admin_client.post(url, data=form)
    assert response.status_code == HTTPStatus.NOT_FOUND
    note_from_db = Note.objects.get(id=note.id)
    assert note.title == note_from_db.title
    assert note.text == note_from_db.text


def test_author_can_delete(author_client, note):
    url = reverse('notes:delete', args=(note.id,))
    response = author_client.delete(url)
    assertRedirects(response, reverse('notes:list'))
    count = Note.objects.all()
    assert count.count() == 0


def test_other_cant_delete(admin_client, note):
    url = reverse_lazy('notes:delete', args=(note.id,))
    response = admin_client.delete(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    count = Note.objects.all()
    assert count.count() == 1
