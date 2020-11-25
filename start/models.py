from django.db import models
from django.contrib.auth.models import User
from random import randint
from django.db.models.signals import post_save
from .tasks import qeydiyyat_maili

class activateProfile(models.Model):
    useri       = models.OneToOneField(User,null=True,blank=False,on_delete = models.CASCADE)
    code        = models.IntegerField(null=True,blank=True,default=0) 
    status      = models.BooleanField(null=True,blank=False,default=False)

    def __str__(self):
        return self.useri.username

def codegonder(sender,instance,created,*args,**kwargs):
    if created:
        newActivateProfile = activateProfile(useri = instance)
        newActivateProfile.code = randint(100000,999999)
        newActivateProfile.save()
        mesaj = """
            Qeydiyyatiniz ugurla basa catmisdir,Hormetli : {}.
            Aktivasiya kodu : {}
        """.format(instance.username,newActivateProfile.code)
        email = instance.email
        qeydiyyat_maili.delay("Tesekkurler",mesaj,"todoapp98@gmail.com",[email,])


post_save.connect(codegonder,sender =  User,)


class loglogin(models.Model):
    browser   = models.CharField(max_length=400,null=True,blank=False)
    os        = models.CharField(max_length=400,null=True,blank=False)
    device    = models.CharField(max_length=400,null=True,blank=False)
    useri     = models.CharField(max_length=250,null=True,blank=False)

    def __str__(self):
        return self.browser
