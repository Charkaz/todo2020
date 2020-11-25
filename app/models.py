from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .tasks import todo_yaratma_maili,son10deq
from datetime import datetime,timedelta
# Create your models here.

class todo(models.Model):
    basliq         = models.CharField(max_length=150,null=True,blank=False) 
    aciqlama       = models.TextField(max_length=150,null=True,blank=False)
    yaranma_tarix  = models.DateTimeField(auto_now_add=True)
    bitme_tarixi   = models.DateTimeField(null=True,blank=False)
    useri          = models.ForeignKey(User,null=True,blank=False,on_delete = models.CASCADE)
    def __str__(self):
        return self.basliq


def mail_bildirim_gonder(sender,instance,created,*args,**kwargs):
    if created:
        mesaj = """
           Hormetli istifadeci sizin  todo' ugurla yaradildi,
           tebrik edirik.
           1) Todo-nun basliqi - {}
           2) Todo-nun yekunlasma tarixi - {}

        """.format(instance.basliq,instance.bitme_tarixi)
        email = instance.useri.email
        
        todo_yaratma_maili.delay("Tebrikler",mesaj,"todoapp98@gmail.com",[email,])
        hesabla = (instance.bitme_tarixi - instance.yaranma_tarix)-timedelta(minutes=10)
        saniye = int(hesabla.total_seconds())
        print(saniye)
        mesaj2 = """
           sizin {}-basliqli todunuzun son tarixine 10 deq qalib,
        """.format(instance.basliq)
        son10deq.delay(saniye,mesaj2,[email,])
        

post_save.connect(mail_bildirim_gonder,sender =  todo,)

class todopaylas(models.Model):
    todom        = models.ForeignKey(todo,null=True,blank=False,on_delete = models.CASCADE)
    paylasan_id  = models.ForeignKey(User,null=True,blank=False,on_delete = models.CASCADE,related_name='paylasan_id',db_column='paylasan_id')
    alan_id      = models.ForeignKey(User,null=True,blank=False,on_delete = models.CASCADE,related_name='alan_id',db_column='alan_id')
    rey_icaze    = models.BooleanField(null=True,blank=False,default=False)
    tesdiq       = models.BooleanField(null=True,blank=False,default=False)


    def __str__(self):
        string = "{}-{}-{}".format(self.todom.basliq,self.paylasan_id.username,self.alan_id.username)
        return string

def todopaylasilan(sender,instance,created,*args,**kwargs):
    if created:
        try:
            yenitodopaylas = todopaylas.objects.create(todom=instance,paylasan_id = instance.useri,alan_id=instance.useri,rey_icaze=True,tesdiq=True)
        except Exception as e:
            print(e)
post_save.connect(todopaylasilan,sender =  todo,)


class serh(models.Model):
    metin   = models.CharField(max_length=350,null=True,blank=False)
    todom   = models.ForeignKey(todo,null=True,blank=False,on_delete=models.CASCADE)
    tarix   = models.DateTimeField(auto_now_add=True)
    useri   = models.ForeignKey(User,null=True,blank=False,on_delete=models.CASCADE)

    def __str__(self):
        return self.metin 