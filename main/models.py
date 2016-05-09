# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import random
import string
import time
from django.contrib.auth.models import User
from django.db import models

from inviter.settings import INVITE_CODE_LENGTH


def generate_invite_code():
    return ("%.10d" % int(time.time()))[:10] + \
           ''.join(random.choice(string.digits)
                   for _ in xrange(INVITE_CODE_LENGTH - 10))


class Invite(models.Model):
    code = models.CharField(primary_key=True,
                            max_length=INVITE_CODE_LENGTH,
                            default=generate_invite_code)
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=False,
                              unique=True)
    sent_date = models.DateTimeField()
