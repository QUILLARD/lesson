from django.contrib import admin

from testapp.models import SMS, Img


class SMSAdmin(admin.ModelAdmin):
    list_display = ['id', 'comment', 'sender', 'receiver']
    list_display_links = ['id', 'comment']


admin.site.register(SMS, SMSAdmin)
admin.site.register(Img)
