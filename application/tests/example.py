#!/usr/bin/env python3
import unittest

from main import app


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False

        # Create the test client
        self.client = app.test_client()

        # Propogate exceptions to the test client
        self.client.testing = True

    def tearDown(self):
        pass

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
