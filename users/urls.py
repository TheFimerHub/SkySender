from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, VerifyEmailSentView, VerifyEmailAcceptedView, \
    UserResetPasswordView, UserResetPasswordSuccessView, UserInactiveView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('verify-email/', VerifyEmailSentView.as_view(), name='verify-email-sent'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailAcceptedView.as_view(), name='verify-email-accepted'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('reset-password/', UserResetPasswordView.as_view(), name='reset-password'),
    path('reset-password-success', UserResetPasswordSuccessView.as_view(), name='reset-password-success'),
    path('inactive/', UserInactiveView.as_view(), name='inactive-user')
]
