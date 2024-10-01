import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsboard.settings')

app = Celery('newsboard')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()




app.conf.beat_schedule = {
    'scheduled_mailing_every_monday_8am': {
        'task': 'tasks.scheduled_mailing',
        'schedule': crontab(hour = 8, minute = 0, day_of_week = 'monday'),
        'args': ("some_arg"),
    },

   'action_every_30_seconds': {
        'task': 'tasks.hello',
        'schedule': 30,
        'args': ("some_arg"),
    },
}