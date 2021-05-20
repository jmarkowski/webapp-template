#!/usr/bin/env python3
import datetime
import unittest

from util.email import parse_email
from util.email import InvalidEmail


class UtilTimeTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_valid_email(self):
        email = 'foo@example.com'

        self.assertTrue(parse_email(email))

    def test_maximum_allowed_email_length(self):
        email = 'a' * 64 + '@' + 'b' * 185 + '.com'

        self.assertTrue(parse_email(email))

    def test_email_parts(self):
        email = 'foo@bar.com'

        local, domain, tld = parse_email(email)

        self.assertEqual('foo', local)
        self.assertEqual('bar', domain)
        self.assertEqual('com', tld)

    def test_email_parts_complex(self):
        email = 'john.doe@example-domain.co.uk'

        local, domain, tld = parse_email(email)

        self.assertEqual('john.doe', local)
        self.assertEqual('example-domain', domain)
        self.assertEqual('co.uk', tld)

    def test_parsing_invalid_email(self):
        email = 'invalid-email'

        with self.assertRaises(InvalidEmail):
            parse_email(email)

    def test_parsing_none(self):
        with self.assertRaises(InvalidEmail):
            parse_email(None)

    def test_invalid_email_missing_tld(self):
        email = 'foo@example'

        with self.assertRaises(InvalidEmail):
            parse_email(email)

    def test_invalid_email_missing_domain(self):
        email = 'foo@.com'

        with self.assertRaises(InvalidEmail):
            parse_email(email)

    def test_invalid_email_missing_local_part(self):
        email = '@example.com'

        with self.assertRaises(InvalidEmail):
            parse_email(email)

    def test_invalid_email_missing_at_symbol(self):
        email = 'foo.example.com'

        with self.assertRaises(InvalidEmail):
            parse_email(email)

    def test_invalid_email_multiple_at_symbols(self):
        email = 'foo@bar@example.com'

        with self.assertRaises(InvalidEmail):
            parse_email(email)

    def test_invalid_email_local_part_too_long(self):
        email = 'a' * 65 + '@example.com'

        with self.assertRaises(InvalidEmail):
            parse_email(email)

    def test_invalid_email_domain_too_long(self):
        email = 'foo@' + 'a' * 252 + '.com'

        with self.assertRaises(InvalidEmail):
            parse_email(email)


if __name__ == '__main__':
    unittest.main()
