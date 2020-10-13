#!/usr/bin/env python3
import unittest

from config import config_map
from core.database import init_db_session
from core.database import deinit_db_session
from core.gateway import InvitationDataGateway
from core.invitation import InvitationInteractor


class InvitationInteractorTests(unittest.TestCase):

    def setUp(self):
        config = config_map['testing']
        self.db = init_db_session(config.DB_URI, echo_raw_sql=False)
        self.interactor = InvitationInteractor(InvitationDataGateway(self.db))

    def tearDown(self):
        deinit_db_session(self.db)

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
