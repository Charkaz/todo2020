from django.shortcuts import render,HttpResponseRedirect,reverse,HttpResponse
from .forms import TodoForm,serhupdateForm
from .models import todo,serh
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.models import User
from .models import todopaylas
from django.db.models import Q
# Create your views here.


def room(request, room_name):
    #sta = mesaj.objects.all()
    return render(request, 'chatroom.html', {
        'room_name': room_name,
    })


@login_required(login_url=reverse_lazy('login'))
def yeniTodo(request):
    form  = TodoForm(request.POST or None)
    if form.is_valid():
        basliq         = form.cleaned_data.get('basliq')
        aciqlama       = form.cleaned_data.get('aciqlama')
        son_tarix      = form.cleaned_data.get('son_tarix')
        try:
            yeniTodo   = todo.objects.create(basliq=basliq,aciqlama=aciqlama,bitme_tarixi=son_tarix,useri=request.user) 
            messages.success(request,"Yeni Todo ugurla yaradildi ",extra_tags='success')
            return HttpResponseRedirect(reverse('dashboard'))
        except Exception as e:
            messages.success(request,"Todo yaradilarken problem yarandi " +str(e),extra_tags='danger')
            return HttpResponseRedirect(reverse('dashboard'))
        return HttpResponseRedirect(reverse('dashboard'))


@login_required(login_url=reverse_lazy('login'))
def tododetail(request,id):
    try:
        todom = todo.objects.get(id = id)
        
        alanlar = False
        for i in todopaylas.objects.filter(todom=todom):
            if i.alan_id == request.user:
                alanlar = True
            
        form  = TodoForm(request.POST or None)
        users   = User.objects.filter()
        serhler = serh.objects.filter(todom= todom)
        icaze = todopaylas.objects.get(todom=todom,alan_id=request.user)
        context = {
            'todom':todom,
            'form':form,
            'users':users,
            'serhler':serhler,
            'icaze':icaze,
        }
        if not alanlar:
            return HttpResponse("bu sehifeye baxmaginiza icaze yoxdur.")

        return render(request,'tododetail.html',context)
    except Exception as e:
        messages.success(request,"Bele todo yoxdur."+" "+str(e),extra_tags='warning')
        return HttpResponseRedirect(reverse('dashboard'))


@login_required(login_url=reverse_lazy('login'))
def todoUpdate(request,id):
    if request.method == 'POST':
        basliq    = request.POST['basliq']
        aciqlama  = request.POST['aciqlama']
        son_tarix = request.POST['son_tarix']
        il = son_tarix.split('-')[0]
        ay =son_tarix.split('-')[1]
        gun =son_tarix.split('-')[2][:2]
        saat = son_tarix.split('-')[2][3:5]
        deq = son_tarix[14:]
        bitme_tarixi = datetime(year=int(il),month=int(ay),day=int(gun),hour=int(saat),minute=int(deq))
        try:
            todom = todo.objects.get(id = id)
            todom.basliq       = basliq
            todom.aciqlama     = aciqlama
            todom.bitme_tarixi = bitme_tarixi
            todom.save()
            messages.success(request,"Ugurla deyisdirildi.",extra_tags='success')
            return HttpResponseRedirect(reverse('dashboard'))
        except:
            print('problem yarandi')
            return HttpResponse(id)


@login_required(login_url=reverse_lazy('login'))
def paylas(request,id):
    if request.method == 'POST':
        secilen_user = request.POST['user']
        icaze        = False
        try:
            if request.POST['icaze']:
                icaze = True
        except:
            icaze = False
        try:
            paylasan = request.user
            alan     = User.objects.get(id = int(secilen_user))
            todom    = todo.objects.get(id = id)
            if todopaylas.objects.filter(todom=todom,alan_id=alan):
                mesaj = "Bu todo {} - ile daha evvel paylasilib.".format(alan.username)
                messages.success(request,mesaj,extra_tags='info')
                return HttpResponseRedirect(reverse('dashboard'))
            paylasim = todopaylas.objects.create(todom=todom,paylasan_id=paylasan,alan_id = alan,rey_icaze = icaze)
            messages.success(request,"Todo'nu ugurla paylasdiniz.",extra_tags='success')
            return HttpResponseRedirect(reverse('dashboard'))
        except Exception as e:
            messages.success(request,"Todo'nu paylasarken problem yarandi."+" "+str(e),extra_tags='danger')
            return HttpResponseRedirect(reverse('dashboard'))
        
@login_required(login_url=reverse_lazy('login'))
def isteksil(request,id):
    try:
        todoistek = todopaylas.objects.get(id = id)
        todoistek.delete()
        messages.success(request,"Todo isdeyi redd edildi.",extra_tags='success')
        return HttpResponseRedirect(reverse('dashboard'))
    except Exception as e:
        messages.success(request,"Todo isdeyi redd edilmedi.",extra_tags='danger')
        return HttpResponseRedirect(reverse('dashboard'))


@login_required(login_url=reverse_lazy('login'))
def istekqebul(request,id):
    try:
        todoistek = todopaylas.objects.get(id = id)
        todoistek.tesdiq  = True
        todoistek.save()
        messages.success(request,"Todo isdeyi Qebul edildi.",extra_tags='success')
        return HttpResponseRedirect(reverse('dashboard'))
    except Exception as e:
        messages.success(request,"Todo isdeyi qebul edilmedi.",extra_tags='danger')
        return HttpResponseRedirect(reverse('dashboard'))


@login_required(login_url=reverse_lazy('login'))
def axtaris(request):
    axtar = request.GET['q']
    print(axtar)
    form    = TodoForm(request.POST or None)
   
    paylasilan_todolar = todopaylas.objects.filter(
        Q(todom__basliq__icontains = axtar) | Q(todom__aciqlama__icontains = axtar)
        ,alan_id = request.user,tesdiq=True)
    #paylasilan_todolar = todopaylas.objects.filter(todom__basliq__icontains ='ay',alan_id = request.user,tesdiq=True)
    paylasilan_todolar_gozleyenler = todopaylas.objects.filter(alan_id = request.user,tesdiq=False)
    istek_sayi  = todopaylas.objects.filter(alan_id = request.user,tesdiq=False).count() 
    context = {
        'form':form,
        'paylasilanlar':paylasilan_todolar,
        'istek_sayi':istek_sayi,
        'paylasilan_todolar_gozleyenler':paylasilan_todolar_gozleyenler,
     
    }
    return render(request,'dashboard.html',context)


@login_required(login_url=reverse_lazy('login'))
def serhsil(request,id):
    serhim = serh.objects.get(id = id)
    todom = serhim.todom
    if not (serhim.useri == request.user or todom.useri == request.user):
        messages.success(request,"Bu sehifeye giris icazeniz yoxdur.",extra_tags='warning')
        return HttpResponseRedirect(reverse("dashboard"))
    try:
        serhim = serh.objects.get(id = id)
        todom  = serhim.todom
        serhim.delete()
        messages.success(request,"yazdiginiz serhi sildiniz .",extra_tags='info')
        return HttpResponseRedirect(reverse('tododetail',kwargs={'id':todom.id}))
    except Exception as e:
        messages.success(request,"problem yarandi ."+str(e),extra_tags='danger')
        return HttpResponseRedirect(reverse('dashboard'))


@login_required(login_url=reverse_lazy('login'))
def serhupdate(request,id):
    serhim = serh.objects.get(id = id)
    todom = serhim.todom
    if not (serhim.useri == request.user):
        messages.success(request,"Bu sehifeye giris icazeniz yoxdur.",extra_tags='warning')
        return HttpResponseRedirect(reverse("dashboard"))
    if request.method == "POST":
        
        metin = request.POST['serh']
        try:
            serhim.metin = metin
            serhim.save()
            messages.success(request,"yazdiginiz serh ugurla deyisdirildi.",extra_tags = "success")
            return HttpResponseRedirect(reverse('tododetail',kwargs={'id':todom.id}))
        except Exception as e:
            print("problem yarandi."+str(e))
    context ={
        'serh':serhim,
        }
    return render(request,'serhupdate.html',context)
   
        