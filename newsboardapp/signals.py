from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from .models import Post
from django.core.mail import send_mail,mail_managers
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .tasks import hello, send_mail_onpost

@receiver(post_save, sender=Post)
def notify_managers_appointment(sender, instance, created, **kwargs):
    send_mail_onpost.delay(instance, created)
    mail_managers(
        subject=instance.caption,
        message=instance.message,
    )


