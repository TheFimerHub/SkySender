from django.contrib import admin
from .models import Client, Message, Mailing, Attempt

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'name')
    search_fields = ('email', 'name')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject',)
    search_fields = ('subject',)

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('message', 'start_time', 'periodicity', 'status')
    search_fields = ('message__subject',)
    list_filter = ('periodicity', 'status')

@admin.register(Attempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'attempt_time', 'status')
    search_fields = ('mailing__message__subject',)
    list_filter = ('status',)
