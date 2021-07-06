import unittest
from app import create_app
from app.db import db


class BaseTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app('testing')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self) -> None:
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
