#!/usr/bin/env python3
import unittest

from flask import current_app
from webapp import create_app


class TestCase(unittest.TestCase):
    def setUp(self):
        test_settings = {
            'TESTING': True,
            'DEBUG': False,
        }

        self.app = create_app(override_settings=test_settings)

        # Create the test client
        self.client = self.app.test_client()

        # Propogate exceptions to the test client
        self.client.testing = True

        # Bind the application context to the current context.
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_route_to_index(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(200, response.status_code)

    def test_json_api_debug_config(self):
        var = 'debug'
        response = self.client.get('/config/{}'.format(var))
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.is_json)
        self.assertDictEqual({'debug': False}, response.get_json())

    def test_json_api_testing_config(self):
        var = 'testing'
        response = self.client.get('/config/{}'.format(var))
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.is_json)
        self.assertDictEqual({'testing': True}, response.get_json())


if __name__ == '__main__':
    unittest.main()
