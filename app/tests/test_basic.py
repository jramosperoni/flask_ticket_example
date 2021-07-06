from . import BaseTestCase


class BasicTestCase(BaseTestCase):
    def test_main_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
