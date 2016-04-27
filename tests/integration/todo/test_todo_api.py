import pytest
from django.core.urlresolvers import reverse

from todo.models import Todo

pytestmark = pytest.mark.django_db


@pytest.fixture
def todo_data(bob_barker):
    return {
      'user': bob_barker.id,
      'completed': False,
      'name': 'My Todo Item',
    }


def test_list(client, bob_barker, incomplete_todo, completed_todo, buy_milk):
    client.login(bob_barker)
    url = reverse('todo-list')
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert all([bob_barker.id == d['user'] for d in data])


def test_create(client, bob_barker, todo_data):
    client.login(bob_barker)
    url = reverse('todo-list')
    response = client.post(url, todo_data)
    assert response.status_code == 201
    todo = Todo.objects.get()
    assert todo.id == response.json()['id']
    assert todo.user == bob_barker


def test_delete(client, bob_barker, buy_milk):
    client.login(bob_barker)
    url = reverse('todo-detail', kwargs={'pk': buy_milk.id})
    response = client.delete(url)
    assert response.status_code == 204
    assert Todo.objects.count() == 0


def test_complete(client, bob_barker, incomplete_todo):
    client.login(bob_barker)
    url = reverse('todo-detail', kwargs={'pk': incomplete_todo.id})
    response = client.patch(url, {'completed': True})
    assert response.status_code == 200
    assert Todo.objects.filter(completed=True).count() == 1
    assert Todo.objects.filter(completed=False).count() == 0


def test_access(client, bob_barker, vana_white, alex_trebek, buy_milk):
    client.login(vana_white)

    url = reverse('todo-list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 0

    url = reverse('todo-detail', kwargs={'pk': buy_milk.id})
    response = client.delete(url)
    assert response.status_code == 404
    assert Todo.objects.filter(id=buy_milk.id).exists()

    response = client.patch(url, {'completed': True})
    assert response.status_code == 404
    assert Todo.objects.filter(id=buy_milk.id, completed=False).exists()

    client.login(alex_trebek)

    url = reverse('todo-list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 1

    url = reverse('todo-detail', kwargs={'pk': buy_milk.id})
    response = client.patch(url, {'completed': True})
    assert response.status_code == 200
    assert Todo.objects.filter(id=buy_milk.id, completed=True).exists()

    response = client.delete(url)
    assert response.status_code == 204
    assert not Todo.objects.exists()
