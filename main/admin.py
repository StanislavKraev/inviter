from django.contrib import admin

from main.models import Invite


class InviteAdminModel(admin.ModelAdmin):

    fields = ('email',)
    list_display = ('email', 'code', 'user', 'sent_date')
    ordering = ('email',)

admin.site.register(Invite, InviteAdminModel)
