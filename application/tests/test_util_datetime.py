#!/usr/bin/env python3
import datetime
import unittest

from util.datetime import now_str


class UtilTimeTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_now_str_default(self):
        fmt = '%Y-%m-%d, %H:%M:%S'

        exp = datetime.datetime.now().strftime(fmt)
        act = now_str()

        self.assertEqual(exp, act)

    def test_now_str_with_custom_fmt(self):
        fmt = '%d %a %B, %Y'
        exp = datetime.datetime.now().strftime(fmt)
        act = now_str(fmt)

        self.assertEqual(exp, act)


if __name__ == '__main__':
    unittest.main()
