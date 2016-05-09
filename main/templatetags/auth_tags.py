# -*- coding: utf-8 -*-

from django import template
from django.contrib.auth.forms import AuthenticationForm

register = template.Library()


@register.inclusion_tag('tags/auth_block.html')
def auth_block(context):
    current_user = context['user']
    form = AuthenticationForm()
    return {
        'auth_form': form,
        'user': current_user
    }
