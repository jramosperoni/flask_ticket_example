from http import HTTPStatus
import json
from . import BaseTestCase


class UserTestCase(BaseTestCase):
    endpoint = '/users/'
    user_mock = {'first_name': 'First Name',
                 'last_name': 'Last Name',
                 'username': 'Username',
                 'password': 'test'}
    edited_user_mock = {'first_name': 'Edited First Name',
                        'last_name': 'Edited Last Name',
                        'username': 'Edited Username'}

    def test_get_users(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(json.loads(response.data), [])

    def test_get_user(self):
        expected_user = self.client.post(self.endpoint, json=self.user_mock)
        response = self.client.get(f"{self.endpoint}{json.loads(expected_user.data).get('id')}")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data, expected_user.data)

    def test_get_user_not_found(self):
        response = self.client.get(f"{self.endpoint}1")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_create_user(self):
        response = self.client.post(self.endpoint, json=self.user_mock)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertIn(b'id', response.data)
        self.assertIn(b'role', response.data)
        self.assertIn(b'deleted', response.data)
        self.assertGreater(json.loads(response.data).items(),
                           {key: value for key, value in self.user_mock.items() if key != 'password'}.items())

    def test_create_user_bad_request(self):
        response = self.client.post(self.endpoint, json={key: value for key, value in self.user_mock.items()
                                                         if key != 'username'})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn(b'username', response.data)

    def test_create_user_unique_constraint(self):
        response = self.client.post(self.endpoint, json=self.user_mock)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        response = self.client.post(self.endpoint, json=self.user_mock)
        self.assertEqual(response.status_code, HTTPStatus.CONFLICT)
        self.assertIn(b'username', response.data)

    def test_update_user(self):
        user = self.client.post(self.endpoint, json=self.user_mock)
        response = self.client.put(f"{self.endpoint}{json.loads(user.data).get('id')}", json=self.edited_user_mock)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(b'id', response.data)
        self.assertIn(b'role', response.data)
        self.assertIn(b'deleted', response.data)
        self.assertGreater(json.loads(response.data).items(), self.edited_user_mock.items())

    def test_update_user_bad_request(self):
        user = self.client.post(self.endpoint, json=self.user_mock)
        response = self.client.put(f"{self.endpoint}{json.loads(user.data).get('id')}", json={**self.edited_user_mock,
                                                                                              'username': ''})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn(b'username', response.data)

    def test_update_user_unique_constraint(self):
        user_1 = self.client.post(self.endpoint, json=self.user_mock)
        self.assertEqual(user_1.status_code, HTTPStatus.CREATED)
        user_2 = self.client.post(self.endpoint, json={**self.edited_user_mock, 'password': 'test'})
        self.assertEqual(user_2.status_code, HTTPStatus.CREATED)
        response = self.client.put(f"{self.endpoint}{json.loads(user_2.data).get('id')}",
                                   json={**self.edited_user_mock, 'username': json.loads(user_1.data).get('username')})
        self.assertEqual(response.status_code, HTTPStatus.CONFLICT)
        self.assertIn(b'username', response.data)

    def test_update_user_not_found(self):
        response = self.client.put(f"{self.endpoint}1", json=self.edited_user_mock)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_delete_user(self):
        user = self.client.post(self.endpoint, json=self.user_mock)
        response = self.client.delete(f"{self.endpoint}{json.loads(user.data).get('id')}")
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def test_delete_user_not_found(self):
        response = self.client.delete(f"{self.endpoint}1")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
