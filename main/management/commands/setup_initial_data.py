from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from django.db import transaction

from blog.models import Blog
from main.models import Mailing, Message, Client

User = get_user_model()


class Command(BaseCommand):
    help = 'Setup initial data for the project'

    def handle(self, *args, **kwargs):
        self.stdout.write('Setting up initial data...')

        # Delete existing data (optional, use with caution)
        self.delete_existing_data()

        # Create the manager group if it doesn't exist
        manager_group, created = Group.objects.get_or_create(name='manager')

        if created:
            self.stdout.write(self.style.SUCCESS('Manager group created'))
        else:
            self.stdout.write(self.style.WARNING('Manager group already exists'))

        # Assign permissions to the manager group
        try:
            # Assuming 'view_any_mailing' and other permissions are defined in Mailing model
            permissions = Mailing._meta.permissions

            for codename, description in permissions:
                permission = Permission.objects.get(codename=codename)
                manager_group.permissions.add(permission)

            self.stdout.write(self.style.SUCCESS('Permissions assigned to manager group'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error assigning permissions: {e}'))

        # Create admin user
        admin_user = User.objects.create(
            email='admin',
            pk=1
        )
        password = 'admin'
        admin_user.set_password(password)
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.save()
        self.stdout.write(self.style.SUCCESS('Admin user created'))

        # Create manager user
        manager_user = User.objects.create(
            email='manager',
            pk=2
        )

        password = 'manager'
        manager_user.set_password(password)
        manager_user.groups.add(manager_group)
        manager_user.is_staff = True
        manager_user.save()
        self.stdout.write(self.style.SUCCESS('Manager user created'))

        # Create regular user

        regular_user = User.objects.create(
            email='user',
            pk=3
        )
        password = 'user'
        regular_user.set_password(password)
        regular_user.save()
        self.stdout.write(self.style.SUCCESS('Regular user created'))

        # Load fixtures
        fixtures = [
            'fixtures/blog_data.json',
            'fixtures/clients_data.json',
            'fixtures/messages_data.json',
            'fixtures/mailing_data.json',
        ]

        for fixture in fixtures:
            try:
                call_command('loaddata', fixture)
                self.stdout.write(self.style.SUCCESS(f'Successfully loaded {fixture}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error loading {fixture}: {e}'))

        self.stdout.write(self.style.SUCCESS('All initial data setup complete.'))

    def delete_existing_data(self):
        """
        Deletes all existing data before setting up initial data.
        Use with caution in production.
        """
        with transaction.atomic():
            User.objects.all().delete()
            Group.objects.all().delete()
            Blog.objects.all().delete()
            Mailing.objects.all().delete()
            Message.objects.all().delete()
            Client.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Existing data deleted.'))
