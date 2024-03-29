#!/usr/bin/env python3
import unittest
from http import HTTPStatus

from webui import create_app


class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing',
                logger=__name__)

        # Propogate exceptions to the test client
        self.app.testing = True

        # Create the test client
        self.client = self.app.test_client()

        # Bind the application context to the current context.
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_route_to_index(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(HTTPStatus.OK, response.status_code)


if __name__ == '__main__':
    unittest.main()
