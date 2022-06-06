#!/usr/bin/env python3
import logging
import unittest

from config import create_config
from core.dbgateway import DbGateway
from core.interactor import InvitationInteractor


class InvitationInteractorTests(unittest.TestCase):

    def setUp(self):
        self.config = create_config(config_strategy='testing')
        self.db = DbGateway.open_session(self.config.DB_URI, echo_raw_sql=False)

        logger = logging.getLogger(__name__)
        gateway = DbGateway(self.db)
        self.interactor = InvitationInteractor(
            self.config,
            gateway.invitation,
            logger,
        )

    def tearDown(self):
        DbGateway.close_session(self.db)

    def test_adding_email(self):
        email = 'foo@bar.com'

        self.assertFalse(self.interactor.is_email_already_invited(email))

        self.interactor.add_email_to_invite_list(email)

        self.assertTrue(self.interactor.is_email_already_invited(email))

    def test_getting_invitation_list(self):
        self.interactor.add_email_to_invite_list('foo@bar.com')
        self.interactor.add_email_to_invite_list('bar@foo.com')

        email_list = self.interactor.get_invite_list()

        self.assertEqual(2, len(email_list))
        self.assertEqual('foo@bar.com', email_list[0])
        self.assertEqual('bar@foo.com', email_list[1])


if __name__ == '__main__':
    unittest.main()
