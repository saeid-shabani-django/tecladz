from celery import Celery
from django.core.mail import send_mail
from django.conf import settings

app = Celery('config', broker=settings.CELERY_BROKER_URL)

@app.task
def send_activation_email(email, activation_link):
    send_mail(
        'Activate Your Account',
        f'Click to activate: {activation_link}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )