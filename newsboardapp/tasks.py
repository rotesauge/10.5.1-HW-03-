from celery import shared_task
import time
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from .models import Post,Category
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.core.mail import send_mail

@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


@shared_task
def send_mail_onpost(instance,created):
    if created:
        subject = f' post created {instance.caption} {instance.author}'
    else:
        subject = f'post created {instance.caption} {instance.author}'

    html_content = render_to_string(
        'post_created.html',
        {
            'post': instance,
        }
    )
    tolist = []
    categs = instance.сategory.all()
    for categ in categs:
        subs = categ.subscribers.all()
        for sub in subs:
            tolist.append(sub.email)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=instance.text,
        from_email='rotesauge@aiq.ru',
        to=tolist,
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()  # отсылаем

@shared_task
def scheduled_mailing():
    def my_job():
        for user in User.objects.all():
            post_list = []
            for categ in Category.objects.all():
                for sub in categ.subscribers.all():
                    if user == sub:
                        for post in Post.objects.filter(datetime__gt=datetime.now() - timedelta(days=7),
                                                        сategory=categ):
                            post_list.append(post)
            subject = 'new news and article weekly set: '
            msgtext = ''

            for post in post_list:
                msgtext = msgtext + f' post  {post.caption} {post.get_absolute_url()}'

            send_mail(
                subject=subject,
                message=msgtext,
                from_email='rotesauge@aiq.ru',
                recipient_list=[user.email]
            )

