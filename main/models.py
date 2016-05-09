# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import random
import string
import time

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from inviter.settings import INVITE_CODE_LENGTH


def generate_invite_code():
    return ("%.10d" % int(time.time()))[:10] + \
           ''.join(random.choice(string.digits)
                   for _ in xrange(INVITE_CODE_LENGTH - 10))


class Invite(models.Model):
    code = models.CharField(primary_key=True,
                            max_length=INVITE_CODE_LENGTH)
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=False,
                              unique=True)
    sent_date = models.DateTimeField(default=None, null=True)

    @staticmethod
    def create(email, commit=True):
        new_invite = Invite(email=email)
        if commit:
            new_invite.save()
        return new_invite

    def save(self, *args, **kwargs):
        if not self.pk:
            self.pk = generate_invite_code()
            settings.MAILER.send('invite',
                                 [self.email],
                                 context=dict(
                                    code=self.code
                                 ))
        super(Invite, self).save(*args, **kwargs)
