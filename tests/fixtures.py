import pytest
from .factories import UserFactory, TodoFactory


@pytest.fixture
def bob_barker():
    return UserFactory(
      first_name='Bob',
      last_name='Barker',
      is_staff=False,
    )


@pytest.fixture
def vana_white():
    return UserFactory(
      first_name='Vana',
      last_name='White',
      is_staff=False,
    )


@pytest.fixture
def alex_trebek():
    return UserFactory(
      first_name='Alex',
      last_name='Trebek',
      is_staff=True,
    )


@pytest.fixture
def completed_todo(bob_barker):
    return TodoFactory(
      user=bob_barker,
      completed=True,
    )


@pytest.fixture
def incomplete_todo(bob_barker):
    return TodoFactory(
      user=bob_barker,
      completed=False,
    )


@pytest.fixture
def buy_milk(bob_barker):
    return TodoFactory(
      name='Buy Milk',
      user=bob_barker,
      completed=False,
    )
