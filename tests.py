import unittest

from flask import g, url_for

import db
from application import app


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True

        self.client = app.test_client(use_cookies=True)

        self.app_context = app.test_request_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()


class ApplicationTestCase(FlaskTestCase):
    def test_home_page(self):
        resp = self.client.get('/')
        self.assertTrue(b'Feed' in resp.data, "Didn't find welcome message on home page")

    def test_member_page(self):
        resp = self.client.get(url_for('all_members'))
        self.assertTrue(b'All Members' in resp.data)


class DatabaseTestCase(FlaskTestCase):
    @staticmethod
    def execute_sql(resource_name):
        with app.open_resource(resource_name, mode='r') as f:
            g.cursor.execute(f.read())
        g.connection.commit()

    def setUp(self):
        super(DatabaseTestCase, self).setUp()
        db.open_db_connection()
        self.execute_sql('db/create-db.sql')

    def tearDown(self):
        db.close_db_connection()
        super(DatabaseTestCase, self).tearDown()

    def test_add_post(self):
        row_count = db.create_post(6.99, 100, 'Bananas', 'Upland')
        self.assertEqual(row_count, 1)

        test_post = db.find_post(1)
        self.assertIsNotNone(test_post)

        self.assertEqual(test_post['price'], 6.99)
        self.assertEqual(test_post['quantity'], 100)
        self.assertEqual(test_post['product'], 'Bananas')
        self.assertEqual(test_post['loc'], 'Upland')


if __name__ == '__main__':
    unittest.main()
