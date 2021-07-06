from http import HTTPStatus
import json
from . import BaseTestCase


class TicketTestCase(BaseTestCase):
    def test_get_tickets(self):
        response = self.client.get('/tickets/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(json.loads(response.data), [])

    def test_get_ticket(self):
        ticket_mock = {'description': 'Description test',
                       'subject': 'Subject test'}
        expected_ticket = self.client.post('/tickets/', json=ticket_mock)
        response = self.client.get('/tickets/{0}'.format(json.loads(expected_ticket.data).get('id')))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data, expected_ticket.data)

    def test_get_ticket_not_found(self):
        response = self.client.get('/tickets/1')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_create_ticket(self):
        ticket_mock = {'description': 'Description test',
                       'subject': 'Subject test'}
        response = self.client.post('/tickets/', json=ticket_mock)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertIn(b'id', response.data)
        self.assertIn(b'created_at', response.data)
        self.assertGreater(json.loads(response.data).items(), ticket_mock.items())

    def test_create_ticket_bad_request(self):
        ticket_mock = {'description': 'Description test'}
        response = self.client.post('/tickets/', json=ticket_mock)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn(b'subject', response.data)

    def test_update_ticket(self):
        ticket_mock = {'description': 'Description test',
                       'subject': 'Subject test'}
        edited_ticket_mock = {'description': 'Edited description test',
                              'subject': 'Edited subject test'}
        ticket = self.client.post('/tickets/', json=ticket_mock)
        response = self.client.put('/tickets/{0}'.format(json.loads(ticket.data).get('id')), json=edited_ticket_mock)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertGreater(json.loads(response.data).items(), edited_ticket_mock.items())

    def test_update_ticket_bad_request(self):
        ticket_mock = {'description': 'Description test',
                       'subject': 'Subject test'}
        edited_ticket_mock = {'description': 'Edited description test'}
        ticket = self.client.post('/tickets/', json=ticket_mock)
        response = self.client.put('/tickets/{0}'.format(json.loads(ticket.data).get('id')), json=edited_ticket_mock)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn(b'subject', response.data)

    def test_update_ticket_not_found(self):
        edited_ticket_mock = {'description': 'Edited description test',
                              'subject': 'Edited subject test'}
        response = self.client.put('/tickets/1', json=edited_ticket_mock)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_delete_ticket(self):
        ticket_mock = {'description': 'Description test',
                       'subject': 'Subject test'}
        ticket = self.client.post('/tickets/', json=ticket_mock)
        response = self.client.delete('/tickets/{0}'.format(json.loads(ticket.data).get('id')))
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def test_delete_ticket_not_found(self):
        response = self.client.delete('/tickets/1')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
