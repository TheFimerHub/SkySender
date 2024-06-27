from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    ordering = ['email']
    list_display = ['email', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ('email',)
