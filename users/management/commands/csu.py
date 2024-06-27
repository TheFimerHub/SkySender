from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Create a superuser with specified email and password'

    def handle(self, *args, **kwargs):
        email = 'admin'
        password = 'admin'

        user = User.objects.create(
            email=email,
            is_staff=True,
            is_superuser=True,
        )
        user.set_password(password)
        user.save()

        self.stdout.write(self.style.SUCCESS(f'Superuser "{email}" has been successfully created.'))
