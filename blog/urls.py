from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (
    BlogListView, BlogDetailView)

urlpatterns = [
    path('blogs/', cache_page(60)(BlogListView.as_view()), name='blog-list'),
    path('blogs/post/<int:pk>', cache_page(60 * 5)(BlogDetailView.as_view()), name='blog-detail'),
]
