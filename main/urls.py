from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (
    ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView,
    MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView,
    MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView,
    GeneralPageView, CreatorPageView, block_user, disable_mailing, allow_mailing, unblock_user
)

urlpatterns = [
    path('', cache_page(60)(GeneralPageView.as_view()), name='general-page'),
    path('creator/', CreatorPageView.as_view(), name='creator-page'),

    path('block_user/<int:user_id>/', block_user, name='block-user'),
    path('unblock_user/<int:user_id>/', unblock_user, name='unblock-user'),
    path('disable_mailing/<int:mailing_id>/', disable_mailing, name='disable-mailing'),
    path('allow_mailing/<int:mailing_id>/', allow_mailing, name='allow-mailing'),

    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('clients/add/', ClientCreateView.as_view(), name='client-create'),
    path('clients/<int:pk>/edit/', ClientUpdateView.as_view(), name='client-update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client-delete'),

    path('messages/<int:pk>/detail/', MessageDetailView.as_view(), name='message-detail'),
    path('messages/add/', MessageCreateView.as_view(), name='message-create'),
    path('messages/<int:pk>/edit/', MessageUpdateView.as_view(), name='message-update'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message-delete'),

    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing-detail'),
    path('mailings/add/', MailingCreateView.as_view(), name='mailing-create'),
    path('mailings/<int:pk>/edit/', MailingUpdateView.as_view(), name='mailing-update'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing-delete'),
]
