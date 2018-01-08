from celery import shared_task


@shared_task
def tasktest(param):
    return 'The task executed with argument "%s" ' % param
