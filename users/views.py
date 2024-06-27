import random
import string

from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode
from django.views import generic
from rest_framework.exceptions import ValidationError

from sky_sender import settings
from .forms import UserLoginForm, UserRegistrationForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login

from .services.email_send_verify import send_mail_for_verify

User = get_user_model()


class UserInactiveView(generic.TemplateView):
    template_name = 'users/inactive_user.html'


class UserRegistrationView(generic.CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('verify-email-sent')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        user.is_active = False
        send_mail_for_verify(self.request, user)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object
        return context


class VerifyEmailSentView(generic.TemplateView):
    template_name = 'users/verify_sent.html'
    success_url = reverse_lazy('verify-email-accepted')


class VerifyEmailAcceptedView(generic.View):
    template_name = 'users/verify_accepted.html'
    success_url = reverse_lazy('general-page')

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        context = {}

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
        else:
            return redirect('register')

        return render(request, self.template_name, context)

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        return user


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('general-page')


class UserResetPasswordView(generic.View):
    template_name = 'users/password_reset_success.html'

    def get(self, request):
        return render(request, 'users/password_reset.html')

    def post(self, request):
        user_email = request.POST.get('email')
        try:
            user = User.objects.get(email=user_email)
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            user.password = make_password(new_password)
            user.save()
            send_mail(
                subject='Сброс пароля',
                message=f'Вот твой новый пароль: {new_password}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
                fail_silently=False,
            )
            print(new_password)

            return render(request, self.template_name)
        except User.DoesNotExist:
            return render(request, self.template_name,
                          {'error': 'Пользователь с таким адресом электронной почты не существует.'})


class UserResetPasswordSuccessView(generic.TemplateView):
    template_name = 'reset_password_success.html'
    success_url = reverse_lazy('login')
