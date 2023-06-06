import pytest

from notes.models import Note


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def note(author):
    note = Note.objects.create(
        title='Заголовок',
        text='Текст',
        author=author,
    )
    return note


@pytest.fixture
def form():
    return {
        'title': 'Заголовок номер 2',
        'text': 'какой то текст'
    }
