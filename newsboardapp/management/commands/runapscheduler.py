import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from ...models import Post,Category
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.core.mail import send_mail


logger = logging.getLogger(__name__)


def my_job():
    for user in User.objects.all():
        post_list = []
        for categ in Category.objects.all():
            for sub in categ.subscribers.all():
                if user == sub:
                    for post in Post.objects.filter(datetime__gt =datetime.now() - timedelta(days=7),сategory = categ):
                        post_list.append(post)
        subject = 'new news and article weekly set: '
        msgtext = ''

        for post in post_list:
            msgtext = msgtext + f' post  {post.caption} {post.get_absolute_url()}'

        send_mail(
            subject = subject,
            message = msgtext,
            from_email='rotesauge@aiq.ru',
            recipient_list=[user.email]
        )


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(
                day_of_week="sun", hour="00", minute="00"
            ),
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")