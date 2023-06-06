import pytest
from django.urls import reverse


@pytest.mark.parametrize(
    'user, bool',
    (
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('admin_client'), False),
    )
)
def test_note_in_or_notin_object_list(user, note, bool):
    url = reverse('notes:list')
    response = user.get(url)
    object_list = response.context['object_list']
    assert (note in object_list) is bool


@pytest.mark.parametrize(
    'name, arg',
    (
        ('notes:create', False),
        ('notes:edit', True),
    )
)
def test_form_in_page(name, arg, author_client, note):
    url = reverse(name, args=(note.id,) if arg else None)
    response = author_client.get(url)
    assert 'form' in response.context
