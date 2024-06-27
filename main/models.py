from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Client(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    comment = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'


class Mailing(models.Model):
    EVERY_MINUTE = '1 min'
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'

    PERIODICITY_CHOICES = [
        (EVERY_MINUTE, 'Once a minute'),
        (DAILY, 'Once a day'),
        (WEEKLY, 'Once a week'),
        (MONTHLY, 'Once a month'),
    ]

    CREATED = 'created, waiting to be sent'
    SENT = 'sent, waiting for the next one'
    FINISHED = 'finished, failed to send'

    STATUS_CHOICES = [
        (CREATED, 'Created'),
        (SENT, 'Sent'),
        (FINISHED, 'Finished'),
    ]

    start_time = models.DateTimeField()
    periodicity = models.CharField(max_length=30, choices=PERIODICITY_CHOICES)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=CREATED)
    message = models.OneToOneField(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.message.subject} - {self.get_periodicity_display()}"

    class Meta:
        verbose_name = 'Mailing'
        verbose_name_plural = 'Mailings'

        permissions = [
            ("view_any_mailing", "Can view any mailing"),
            ("disable_mailing", "Can disable mailings"),
            ("allow_mailing", "Can allow mailings"),
            ("block_user", "Can block users"),
            ("unblock_user", "Can unblock users"),
        ]


class Attempt(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField()
    server_response = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Attempt for {self.mailing.message.subject} at {self.attempt_time}"

    class Meta:
        verbose_name = 'Attempt'
        verbose_name_plural = 'Attempts'
