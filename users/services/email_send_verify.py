from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from sky_sender import settings

def send_mail_for_verify(request, user):
    current_site = get_current_site(request)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    domain = current_site.domain
    verify_url = f"http://{domain}/users/verify-email/{uid}/{token}/"

    print(verify_url)

    context = {
        'user': user,
        'verify_url': verify_url,
    }

    # Загрузка HTML-шаблона письма
    email_subject = 'Account Verification'
    email_body = render_to_string('users/verify_email_template.html', context)

    # Отправка письма
    email = EmailMessage(
        email_subject,
        email_body,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
    )
    email.content_subtype = "html"  # Устанавливаем тип содержимого как HTML
    email.send()
