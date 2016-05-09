# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


class Mailer(object):

    @staticmethod
    def send(template_name, recipients, context=None):
        try:
            subject = render_to_string('mails/' + template_name + '.subject',
                                       context=context)
            text = render_to_string('mails/' + template_name + '.text',
                                    context=context)
            html = render_to_string('mails/' + template_name + '.html',
                                    context=context)
        except Exception, ex:
            print ex
            return

        from_email = settings.FROM_EMAIL
        email_user = settings.EMAIL_USER
        email_password = settings.EMAIL_PASSWORD

        send_mail(subject, text, from_email, recipients,
                  auth_user=email_user,
                  auth_password=email_password,
                  html_message=html)
