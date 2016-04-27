import pytest

from todo.models import User
from todo.backends import (
  FacebookBackend,
  TokenException,
  NO_TOKEN,
  INVALID_TOKEN,
  BAD_RESPONSE,
  MISSING_ID,
)

pytestmark = pytest.mark.django_db
backend = FacebookBackend()


@pytest.fixture
def response_valid(mocker):
    response = mocker.Mock()
    response.status_code = 200
    response.json = mocker.Mock(
        return_value={'data': {'is_valid': True}}
    )
    return response


@pytest.fixture
def response_invalid(mocker):
    response = mocker.Mock()
    response.status_code = 200
    response.json = mocker.Mock(
      return_value={'data': {'is_valid': False}}
    )
    return response


@pytest.fixture
def response_bad_status(mocker):
    response = mocker.Mock()
    response.status_code = 500
    return response


@pytest.fixture
def user_data():
    return {
      'id': '123234345456567',
      'first_name': 'Bob',
      'last_name': 'Barker',
      'email': 'bob@priceisright.com',
    }


@pytest.fixture
def response_user_data(mocker, user_data):
    response = mocker.Mock()
    response.status_code = 200
    response.json = mocker.Mock(return_value=user_data)
    return response


@pytest.fixture
def response_user_data_missing_id(mocker, user_data):
    response = mocker.Mock()
    response.status_code = 200
    del user_data['id']
    response.json = mocker.Mock(return_value=user_data)
    return response


def test_check_no_token():
    with pytest.raises(TokenException) as e:
        backend._check_token(None)
    assert str(e.value) == NO_TOKEN


def test_check_invalid_token(mocker, response_invalid):
    requests = mocker.patch('todo.backends.requests')
    requests.get = mocker.Mock(return_value=response_invalid)

    with pytest.raises(TokenException) as e:
        backend._check_token(token='abc123')
    assert str(e.value) == INVALID_TOKEN


def test_check_bad_status(mocker, response_bad_status):
    requests = mocker.patch('todo.backends.requests')
    requests.get = mocker.Mock(return_value=response_bad_status)

    with pytest.raises(TokenException) as e:
        backend._check_token(token='abc123')
    assert str(e.value) == BAD_RESPONSE


def test_fetch_user_bad_response(mocker, response_bad_status):
    requests = mocker.patch('todo.backends.requests')
    requests.get = mocker.Mock(return_value=response_bad_status)

    with pytest.raises(TokenException) as e:
        backend._fetch_user_data(token='abc123')
    assert str(e.value) == BAD_RESPONSE


def test_fetch_user_missing_id(mocker, response_user_data_missing_id):
    requests = mocker.patch('todo.backends.requests')
    requests.get = mocker.Mock(return_value=response_user_data_missing_id)

    with pytest.raises(TokenException) as e:
        backend._fetch_user_data(token='abc123')
    assert str(e.value) == MISSING_ID


def test_fetch_user_data(mocker, response_user_data):
    requests = mocker.patch('todo.backends.requests')
    requests.get = mocker.Mock(return_value=response_user_data)


def test_authenticate(mocker, user_data):
    mocker.patch.object(backend, '_check_token', autospec=True)
    mocker.patch.object(backend, '_fetch_user_data', autospec=True, return_value=user_data)
    user = backend.authenticate(token='abc123')

    backend._check_token.assert_called_with('abc123')
    backend._fetch_user_data.assert_called_with('abc123')
    assert user
    assert user.id == user_data['id']
    assert User.objects.filter(id=user_data['id']).count() == 1
    user = User.objects.get(id=user_data['id'])
    assert user.first_name == user_data['first_name']
    assert user.last_name == user_data['last_name']
    assert user.email == user_data['email']
    assert user.access_token == 'abc123'
