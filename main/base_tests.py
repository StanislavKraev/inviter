# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test import TestCase


class BaseTestCase(TestCase):

    TEST_USER_NAME = "test@domain.zz"
    TEST_EMAIL = "test@domain.zz"
    TEST_PASSWORD = "testpassword1"

    def assertAuthorized(self):
        self.assertGreater(User.objects.all().count(), 0)
        user = User.objects.get()
        self.assertEqual(self.client.session['_auth_user_id'], unicode(user.pk))
        return user

    def assertNotAuthorized(self):
        user = User.objects.get()
        if not user:
            return
        if '_auth_user_id' not in self.client.session:
            return
        user_id = self.client.session['_auth_user_id']
        user = User.objects.get(int(user_id))
        self.assertIsNone(user)

    def authorize(self, create_user=False):
        if create_user:
            user = self.create_test_user()
        else:
            user = User.objects.get()
        self.assertIsNotNone(user)
        self.client.login(username=user.username,
                          password=self.TEST_PASSWORD)

    def create_test_user(self):
        user = User.objects.create_user(self.TEST_USER_NAME,
                                        self.TEST_EMAIL,
                                        self.TEST_PASSWORD)
        user.save()
        return user


def authorized(test_func):
    def func(self):
        user = self.create_test_user()
        self.assertIsNotNone(user)
        self.client.login(username=user.username,
                          password=self.TEST_PASSWORD)
        self.current_user = user
        test_func(self)
    return func
