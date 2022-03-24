from http import HTTPStatus
from . import BaseTestCase


class LoginTestCase(BaseTestCase):
    endpoint = '/login/'
    user_mock = {'first_name': 'First Name',
                 'last_name': 'Last Name',
                 'username': 'Username',
                 'password': 'test'}
    credentials_mock = {'username': user_mock.get('username'), 'password': user_mock.get('password')}

    def test_login(self):
        self.client.post('/users/', json=self.user_mock)
        response = self.client.post(self.endpoint, json=self.credentials_mock)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(b'ey', response.data)
        self.assertIn(b'.ey', response.data)

    def test_login_user_not_found(self):
        response = self.client.post(self.endpoint, json=self.credentials_mock)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertIn(b'User not found', response.data)

    def test_login_invalid_password(self):
        self.client.post('/users/', json=self.user_mock)
        response = self.client.post(self.endpoint, json={**self.credentials_mock, 'password': 'test1'})
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertIn(b'Invalid password', response.data)
