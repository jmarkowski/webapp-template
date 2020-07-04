#!/usr/bin/env python3
import unittest

from flask import current_app
from webapp import create_app


class TestCase(unittest.TestCase):
    def setUp(self):
        test_settings = {
            'CUSTOM_CONFIG': 99
        }

        self.app = create_app('testing', override_settings=test_settings)

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

    def test_json_api_testing_var(self):
        response = self.client.get('/config/testing')

        self.assertEqual(200, response.status_code)
        self.assertTrue(response.is_json)
        self.assertDictEqual({'testing': True}, response.get_json())

    def test_json_api_custom_config_var(self):
        response = self.client.get('/config/custom_config')

        self.assertEqual(200, response.status_code)
        self.assertTrue(response.is_json)
        self.assertDictEqual({'custom_config': 99}, response.get_json())


if __name__ == '__main__':
    unittest.main()
