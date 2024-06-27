from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'views', 'date_added',)
    search_fields = ('title', 'content', 'date_added')
