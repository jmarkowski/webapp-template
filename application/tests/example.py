#!/usr/bin/env python3
import unittest

from webapp import create_app


class TestCase(unittest.TestCase):
    def setUp(self):
        test_settings = {
            'TESTING': True,
            'DEBUG': False,
        }

        app = create_app(override_settings=test_settings)

        # Create the test client
        self.client = app.test_client()

        # Propogate exceptions to the test client
        self.client.testing = True

    def tearDown(self):
        pass

    def test_route_to_index(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
