from celery import shared_task
from django.core.mail import send_mail


@shared_task
def adding_task(x, y):
    return x + y

@shared_task
def qeydiyyat_maili(basliq,mesaj,gonderen,alan):
    send_mail(basliq,mesaj,gonderen, alan)
    return None
    