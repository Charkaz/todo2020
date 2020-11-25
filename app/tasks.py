from celery import shared_task
from django.core.mail import send_mail
from time import sleep


@shared_task
def todo_yaratma_maili(basliq,mesaj,gonderen,alan):
    send_mail(basliq,mesaj,gonderen, alan)
    return None

@shared_task
def son10deq(x,mesaj,alan):
    sleep(x)
    send_mail('Hormetli istifadeci : son 10 deq',mesaj,'todoapp98@gmail.com', alan)
    return None