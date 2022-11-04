from http import HTTPStatus
import json
from unittest.mock import patch
from . import BaseTestCase
from app.auth.models import User, Role, Group
from app.db import db


class TicketTestCase(BaseTestCase):
    admin_role = Role(name='Admin', allowances={'ticket': ['create', 'read', 'update', 'delete']})
    adviser_role = Role(name='Adviser', allowances={'ticket': ['read', 'update']})
    client_role = Role(name='Client', allowances={'ticket': ['create', 'read', 'update', 'delete']})

    @patch('app.login.routes.get_user')
    def test_get_tickets(self, get_user_mock):
        get_user_mock.return_value = User(username='admin', password='test')
        token = self.client.post('/login/', json={'username': 'admin', 'password': 'test'})
        response = self.client.get('/tickets/', headers={'Authorization': f'Bearer {token.json}'})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(json.loads(response.data), [])

    @patch('app.login.routes.get_user')
    def test_get_ticket(self, get_user_mock):
        get_user_mock.return_value = User(username='admin', password='test', roles=[self.admin_role])
        ticket_mock = {'description': 'Description test',
                       'subject': 'Subject test'}
        token = self.client.post('/login/', json={'username': 'admin', 'password': 'test'})
        expected_ticket = self.client.post('/tickets/', json=ticket_mock,
                                           headers={'Authorization': f'Bearer {token.json}'})
        response = self.client.get('/tickets/{0}'.format(json.loads(expected_ticket.data).get('id')),
                                   headers={'Authorization': f'Bearer {token.json}'})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data, expected_ticket.data)

    @patch('app.login.routes.get_user')
    def test_get_ticket_not_found(self, get_user_mock):
        get_user_mock.return_value = User(username='admin', password='test')
        token = self.client.post('/login/', json={'username': 'admin', 'password': 'test'})
        response = self.client.get('/tickets/1', headers={'Authorization': f'Bearer {token.json}'})
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    @patch('app.login.routes.get_user')
    def test_create_ticket_admin(self, get_user_mock):
        get_user_mock.return_value = User(username='admin', password='test', roles=[self.admin_role])
        token = self.client.post('/login/', json={'username': 'admin', 'password': 'test'})
        ticket_mock = {'description': 'Description test',
                       'subject': 'Subject test'}
        response = self.client.post('/tickets/', json=ticket_mock, headers={'Authorization': f'Bearer {token.json}'})
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertIn(b'id', response.data)
        self.assertIn(b'created_at', response.data)
        self.assertGreater(json.loads(response.data).items(), ticket_mock.items())

    @patch('app.login.routes.get_user')
    def test_create_ticket_adviser(self, get_user_mock):
        get_user_mock.return_value = User(username='adviser', password='test', roles=[self.adviser_role])
        token = self.client.post('/login/', json={'username': 'adviser', 'password': 'test'})
        ticket_mock = {'description': 'Description test',
                       'subject': 'Subject test'}
        response = self.client.post('/tickets/', json=ticket_mock, headers={'Authorization': f'Bearer {token.json}'})
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    @patch('app.login.routes.get_user')
    def test_create_ticket_client(self, get_user_mock):
        get_user_mock.return_value = User(username='client', password='test', roles=[self.client_role])
        token = self.client.post('/login/', json={'username': 'client', 'password': 'test'})
        ticket_mock = {'description': 'Description test',
                       'subject': 'Subject test'}
        response = self.client.post('/tickets/', json=ticket_mock, headers={'Authorization': f'Bearer {token.json}'})
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertIn(b'id', response.data)
        self.assertIn(b'created_at', response.data)
        self.assertGreater(json.loads(response.data).items(), ticket_mock.items())

    @patch('app.login.routes.get_user')
    def test_create_ticket_bad_request(self, get_user_mock):
        get_user_mock.return_value = User(username='admin', password='test')
        token = self.client.post('/login/', json={'username': 'admin', 'password': 'test'})
        ticket_mock = {'description': 'Description test'}
        response = self.client.post('/tickets/', json=ticket_mock, headers={'Authorization': f'Bearer {token.json}'})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn(b'subject', response.data)

    @patch('app.login.routes.get_user')
    def test_update_ticket_admin(self, get_user_mock):
        get_user_mock.return_value = User(username='admin', password='test', roles=[self.admin_role])
        token = self.client.post('/login/', json={'username': 'admin', 'password': 'test'})
        ticket_mock = {'description': 'Description test',
                       'subject': 'Subject test'}
        edited_ticket_mock = {'description': 'Edited description test',
                              'subject': 'Edited subject test'}
        ticket = self.client.post('/tickets/', json=ticket_mock, headers={'Authorization': f'Bearer {token.json}'})
        response = self.client.put('/tickets/{0}'.format(json.loads(ticket.data).get('id')), json=edited_ticket_mock,
                                   headers={'Authorization': f'Bearer {token.json}'})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertGreater(json.loads(response.data).items(), edited_ticket_mock.items())

    @patch('app.login.routes.get_user')
    def test_update_ticket_adviser(self, get_user_mock):
        get_user_mock.return_value = User(username='admin', password='test', roles=[self.admin_role])
        token = self.client.post('/login/', json={'username': 'admin', 'password': 'test'})
        ticket_mock = {'description': 'Description test',
                       'subject': 'Subject test'}
        ticket = self.client.post('/tickets/', json=ticket_mock, headers={'Authorization': f'Bearer {token.json}'})
        get_user_mock.return_value = User(username='adviser', password='test', roles=[self.adviser_role])
        token = self.client.post('/login/', json={'username': 'adviser', 'password': 'test'})
        edited_ticket_mock = {'description': 'Edited description test',
                              'subject': 'Edited subject test'}
        response = self.client.put('/tickets/{0}'.format(json.loads(ticket.data).get('id')), json=edited_ticket_mock,
                                   headers={'Authorization': f'Bearer {token.json}'})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertGreater(json.loads(response.data).items(), edited_ticket_mock.items())

    @patch('app.login.routes.get_user')
    def test_update_ticket_client(self, get_user_mock):
        get_user_mock.return_value = User(username='client', password='test', roles=[self.client_role])
        token = self.client.post('/login/', json={'username': 'client', 'password': 'test'})
        ticket_mock = {'description': 'Description test',
                       'subject': 'Subject test'}
        edited_ticket_mock = {'description': 'Edited description test',
                              'subject': 'Edited subject test'}
        ticket = self.client.post('/tickets/', json=ticket_mock, headers={'Authorization': f'Bearer {token.json}'})
        response = self.client.put('/tickets/{0}'.format(json.loads(ticket.data).get('id')), json=edited_ticket_mock,
                                   headers={'Authorization': f'Bearer {token.json}'})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertGreater(json.loads(response.data).items(), edited_ticket_mock.items())

    @patch('app.login.routes.get_user')
    def test_update_ticket_client_other_user(self, get_user_mock):
        get_user_mock.return_value = User(id=1, username='admin', password='test', roles=[self.admin_role])
        token = self.client.post('/login/', json={'username': 'admin', 'password': 'test'})
        ticket_mock = {'description': 'Description test',
                       'subject': 'Subject test'}
        ticket = self.client.post('/tickets/', json=ticket_mock, headers={'Authorization': f'Bearer {token.json}'})
        get_user_mock.return_value = User(id=2, username='client', password='test', roles=[self.client_role])
        token = self.client.post('/login/', json={'username': 'client', 'password': 'test'})
        edited_ticket_mock = {'description': 'Edited description test',
                              'subject': 'Edited subject test'}
        response = self.client.put('/tickets/{0}'.format(json.loads(ticket.data).get('id')), json=edited_ticket_mock,
                                   headers={'Authorization': f'Bearer {token.json}'})
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    @patch('app.login.routes.get_user')
    def test_update_ticket_bad_request(self, get_user_mock):
        get_user_mock.return_value = User(username='admin', password='test', roles=[self.admin_role])
        token = self.client.post('/login/', json={'username': 'admin', 'password': 'test'})
        ticket_mock = {'description': 'Description test',
                       'subject': 'Subject test'}
        edited_ticket_mock = {'description': 'Edited description test'}
        ticket = self.client.post('/tickets/', json=ticket_mock, headers={'Authorization': f'Bearer {token.json}'})
        response = self.client.put('/tickets/{0}'.format(json.loads(ticket.data).get('id')), json=edited_ticket_mock,
                                   headers={'Authorization': f'Bearer {token.json}'})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn(b'subject', response.data)

    @patch('app.login.routes.get_user')
    def test_update_ticket_not_found(self, get_user_mock):
        get_user_mock.return_value = User(username='admin', password='test', roles=[self.admin_role])
        token = self.client.post('/login/', json={'username': 'admin', 'password': 'test'})
        edited_ticket_mock = {'description': 'Edited description test',
                              'subject': 'Edited subject test'}
        response = self.client.put('/tickets/1', json=edited_ticket_mock,
                                   headers={'Authorization': f'Bearer {token.json}'})
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    @patch('app.login.routes.get_user')
    def test_delete_ticket_admin(self, get_user_mock):
        get_user_mock.return_value = User(username='admin', password='test', roles=[self.admin_role])
        token = self.client.post('/login/', json={'username': 'admin', 'password': 'test'})
        ticket_mock = {'description': 'Description test',
                       'subject': 'Subject test'}
        ticket = self.client.post('/tickets/', json=ticket_mock, headers={'Authorization': f'Bearer {token.json}'})
        response = self.client.delete('/tickets/{0}'.format(json.loads(ticket.data).get('id')),
                                      headers={'Authorization': f'Bearer {token.json}'})
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    @patch('app.login.routes.get_user')
    def test_delete_ticket_adviser(self, get_user_mock):
        get_user_mock.return_value = User(username='admin', password='test', roles=[self.admin_role])
        token = self.client.post('/login/', json={'username': 'admin', 'password': 'test'})
        ticket_mock = {'description': 'Description test',
                       'subject': 'Subject test'}
        ticket = self.client.post('/tickets/', json=ticket_mock, headers={'Authorization': f'Bearer {token.json}'})
        get_user_mock.return_value = User(username='adviser', password='test', roles=[self.adviser_role])
        token = self.client.post('/login/', json={'username': 'adviser', 'password': 'test'})
        response = self.client.delete('/tickets/{0}'.format(json.loads(ticket.data).get('id')),
                                      headers={'Authorization': f'Bearer {token.json}'})
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    @patch('app.login.routes.get_user')
    def test_delete_ticket_client(self, get_user_mock):
        get_user_mock.return_value = User(username='client', password='test', roles=[self.client_role])
        token = self.client.post('/login/', json={'username': 'client', 'password': 'test'})
        ticket_mock = {'description': 'Description test',
                       'subject': 'Subject test'}
        ticket = self.client.post('/tickets/', json=ticket_mock, headers={'Authorization': f'Bearer {token.json}'})
        response = self.client.delete('/tickets/{0}'.format(json.loads(ticket.data).get('id')),
                                      headers={'Authorization': f'Bearer {token.json}'})
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    @patch('app.login.routes.get_user')
    def test_delete_ticket_not_found(self, get_user_mock):
        get_user_mock.return_value = User(username='admin', password='test', roles=[self.admin_role])
        token = self.client.post('/login/', json={'username': 'admin', 'password': 'test'})
        response = self.client.delete('/tickets/1', headers={'Authorization': f'Bearer {token.json}'})
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
