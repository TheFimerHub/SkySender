import logging
from datetime import datetime, timedelta
import time

from django.core.mail import send_mail
from django.utils import timezone
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.core.management.base import BaseCommand

from main.models import Mailing, Attempt
from sky_sender import settings

logger = logging.getLogger(__name__)


def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = Mailing.objects.filter(start_time__lte=current_datetime).filter(
        status__in=[Mailing.CREATED, Mailing.SENT])

    for mailing in mailings:
        last_attempt = Attempt.objects.filter(mailing=mailing).order_by('-attempt_time').first()

        if should_send(mailing, last_attempt):
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email for client in mailing.clients.all()],
                    fail_silently=False,
                )

                print('message == True')
                Attempt.objects.create(mailing=mailing, status=True, server_response='Success', owner=mailing.owner)
                mailing.status = Mailing.SENT
                mailing.save()

            except Exception as e:
                print('message == False')
                Attempt.objects.create(mailing=mailing, status=False, server_response=str(e))
                mailing.status = Mailing.FINISHED
                mailing.save()
                return print(e)


def should_send(mailing, last_attempt):
    if mailing.periodicity == Mailing.EVERY_MINUTE:
        return not last_attempt or (timezone.now() - last_attempt.attempt_time >= timedelta(minutes=1))
    elif mailing.periodicity == Mailing.DAILY:
        return not last_attempt or (timezone.now() - last_attempt.attempt_time >= timedelta(days=1))
    elif mailing.periodicity == Mailing.WEEKLY:
        return not last_attempt or (timezone.now() - last_attempt.attempt_time >= timedelta(weeks=1))
    elif mailing.periodicity == Mailing.MONTHLY:
        return not last_attempt or (timezone.now() - last_attempt.attempt_time >= timedelta(days=30))
    return False


def start():
    try:
        scheduler = BackgroundScheduler()

        scheduler.add_job(
            send_mailing,
            trigger=IntervalTrigger(seconds=10),
            id="send_mailing",
            replace_existing=True,
        )
        logger.info("Added job: 'send_mailing'.")

        register_events(scheduler)

        scheduler.start()
        logger.info("Scheduler started.")
    except Exception as e:
        print(e)
        time.sleep(30)


class Command(BaseCommand):
    help = 'Runs APScheduler.'

    def handle(self, *args, **options):
        start()
