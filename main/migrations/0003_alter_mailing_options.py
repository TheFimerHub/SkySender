# Generated by Django 4.2 on 2024-06-26 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_attempt_owner_client_owner_mailing_owner_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailing',
            options={'permissions': [('view_any_mailing', 'Can view any mailing'), ('disable_mailing', 'Can disable mailings'), ('block_user', 'Can block users')], 'verbose_name': 'Mailing', 'verbose_name_plural': 'Mailings'},
        ),
    ]
