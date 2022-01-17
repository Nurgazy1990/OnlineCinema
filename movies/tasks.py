# Create your tasks here

from celery import shared_task
from django.core.mail import send_mail


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

@shared_task
def send_activation_mail(email, code):
    message = f'Ваш код активации: {code}'
    send_mail('Активация аккаунта',
              message,
              'test@gmail.com',
              [email])