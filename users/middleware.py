from django.shortcuts import redirect
from django.urls import reverse


class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_active:
            if request.path != reverse('inactive-user'):  # Избегаем циклического перенаправления
                return redirect(reverse('inactive-user'))

        response = self.get_response(request)
        return response

