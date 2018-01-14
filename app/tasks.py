import logging


from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from doyouremember.celery import app


@app.task(name='send-remember-email')
def send_remember_email(user_id, content):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
        send_mail(
            'Remember your memory',
            'Follow this link to verify your account: ' + content,
            'from@quickpublisher.dev',
            [user.email],
            fail_silently=False,
        )
    except UserModel.DoesNotExist:
        logging.warning("Tried to send an email to non-existing user '%s'" % user_id)
