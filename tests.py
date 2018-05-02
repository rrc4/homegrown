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

    def test_user_page(self):
        resp = self.client.get(url_for('all_users'))
        self.assertTrue(b'All Users' in resp.data)


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
        row_count = db.create_post(5.67, 10, 'lb', 'Carrots', 'Vegetables', 'Sample Description', '2018-04-18')
        self.assertEqual(row_count, 1)

        test_post = db.find_post_by_id(1)
        self.assertIsNotNone(test_post)

        self.assertEqual(test_post['price'], 5.67)
        self.assertEqual(test_post['quantity'], 10)
        self.assertEqual(test_post['unit'], 'lb')
        self.assertEqual(test_post['product'], 'Carrots')
        self.assertEqual(test_post['category'], 'Vegetables')
        self.assertEqual(test_post['description'], 'Sample Description')
        self.assertEqual(test_post['date'], '2018-04-18')


if __name__ == '__main__':
    unittest.main()
