# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import override_settings

from inviter.settings import INVITE_CODE_LENGTH
from main.base_tests import BaseTestCase, authorized, TestMailer
from main.models import Invite


@override_settings(mailer=TestMailer())
class GeneralTestCase(BaseTestCase):

    @authorized
    def test_index_authorized(self):
        response = self.client.get(reverse('inviter:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'Выйти', response.content.decode('utf8'))
        self.assertIn(reverse('inviter:logout'), response.content.decode('utf8'))

    def test_index_anonymous(self):
        response = self.client.get(reverse('inviter:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'Войти', response.content.decode('utf8'))
        self.assertIn(reverse('inviter:login'), response.content.decode('utf8'))

    def test_create_invite(self):
        invite = Invite.create('invited_user@domain.zz', commit=True)
        self.assertIsNotNone(invite)
        self.assertEqual(invite.email, 'invited_user@domain.zz')
        self.assertEqual(len(invite.code), INVITE_CODE_LENGTH)
        self.assertTrue(invite.code.isdigit())
        self.assertIsNone(invite.user)
        self.assertIsNone(invite.sent_date)
        self.assertEqual(len(settings.mailer.sent_letters), 1)

    def test_use_invite(self):
        self.assertEqual(User.objects.count(), 0)
        invite = Invite.create('invited_user@domain.zz', commit=True)
        response = self.client.get(reverse('inviter:use_invite',
                                           kwargs=dict(code=invite.code)))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('inviter:index'))
        self.assertEqual(Invite.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1)
        used_invite = Invite.objects.get()
        user = User.objects.get()
        self.assertEqual(used_invite.user, user)

    def test_use_invite_duplicate(self):
        user = User.objects.create_user('testuser',
                                        'someemail@domain.zz',
                                        'password1')
        invite = Invite.create('someemail@domain.zz', commit=False)
        invite.user = user
        invite.save()
        response = self.client.get(reverse('inviter:use_invite',
                                           kwargs=dict(code=invite.code)))

        self.assertEqual(response.status_code, 400)
        self.assertNotAuthorized()

    def test_authorize(self):
        self.create_test_user()
        response = self.client.post(reverse('inviter:login'), data={
            'username': self.TEST_USER_NAME,
            'password': self.TEST_PASSWORD
        })
        self.assertEqual(response.status_code, 302, response)
        self.assertEqual(response.url, reverse('inviter:index'))
        self.assertAuthorized()

    def test_logout(self):
        self.authorize(create_user=True)
        response = self.client.get(reverse('inviter:logout'))
        self.assertAuthorized()
        self.assertEqual(response.status_code, 405)
        response = self.client.post(reverse('inviter:logout'))
        self.assertNotAuthorized()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('inviter:index'))

    def test_login_page(self):
        response = self.client.get(reverse('inviter:login'))
        self.assertEqual(response.status_code, 200)