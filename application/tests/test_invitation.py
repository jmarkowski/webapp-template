#!/usr/bin/env python3
import unittest

from core.invitation import AbstractInvitationGateway
from core.invitation import InvitationInteractor


class InvitationGateway(AbstractInvitationGateway):

    invite_list = []

    @classmethod
    def add_email(cls, email):
        assert(isinstance(email, str))
        cls.invite_list.append(email)

    @classmethod
    def get_email(cls, email):
        assert(isinstance(email, str))

        if email in cls.invite_list:
            return email
        else:
            return None

    @classmethod
    def get_email_list(cls):
        return cls.invite_list

    @classmethod
    def reset(cls):
        cls.invite_list = []


class InvitationInteractorTests(unittest.TestCase):

    def setUp(self):
        self.interactor = InvitationInteractor(InvitationGateway)

    def tearDown(self):
        InvitationGateway.reset()

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

    def test_getting_invitation_list(self):
        pass


if __name__ == '__main__':
    unittest.main()
