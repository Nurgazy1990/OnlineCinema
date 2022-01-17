from django.contrib.auth import get_user_model

User = get_user_model()

from online_cinema.celery import app
from django.core.mail import send_mail

@app.task
def send_activation_mail(email, code):
    message = f'Ваш код активации: {code}'
    send_mail('Активация аккаунта',
              message,
              'test@gmail.com',
              [email])

@app.task
def send_beat_email():
    for contact in User.objects.all():
        message = f'Это Спам'
        send_mail('Онлайн Кинотеатр',
                  message,
                  'test@gmail.com',
                  [contact.email])

