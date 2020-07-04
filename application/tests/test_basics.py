#!/usr/bin/env python3
import unittest

from flask import current_app
from webapp import create_app


class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')

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

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])


if __name__ == '__main__':
    unittest.main()
