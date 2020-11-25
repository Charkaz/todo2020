from django.shortcuts import render,HttpResponseRedirect,reverse,HttpResponse
from .forms import registerForm,loginForm,ActivationForm
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import activateProfile
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from app.forms import TodoForm
from app.models import todopaylas
from app.models import todo
from user_agents import parse
from .models import loglogin
#asinxron
from .tasks import adding_task,qeydiyyat_maili
# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard')) 
    form = registerForm(request.POST or None)
    if form.is_valid():
        try:
            newUser = User(username=form.cleaned_data.get('Istifadeciadi'),first_name=form.cleaned_data.get('Adi'),last_name=form.cleaned_data.get('Soyadi'),email = form.cleaned_data.get('email'))
            newUser.set_password(form.cleaned_data.get('password'))
            newUser.save()
            messages.success(request,"Istifadeci qeydiyyati gurludur.",extra_tags='success')
            return HttpResponseRedirect(reverse('login'))
        except IntegrityError:
            messages.success(request,"Istifadeci adi mesguldur. ",extra_tags='warning')
    context ={ 
        'form':form,
    }
    return render(request,'index.html',context)

def loginpage(request):
    data = request.META["HTTP_USER_AGENT"]
    ipaddress = request.META.get('REMOTE_ADDR')
    print(ipaddress)
    yekun = parse(data)
    print(yekun.browser,yekun.os,yekun.device)


    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard')) 
    form = loginForm(request.POST or None)
    if form.is_valid():
        istifadeci_adi = form.cleaned_data.get('istifadeci_adi')
        sifre          = form.cleaned_data.get('sifre')
        userim         = authenticate(request,username = istifadeci_adi,password = sifre) 
        if userim is not None:
            yoxla = activateProfile.objects.get(useri=userim)
            login(request,userim)
            loglogin.objects.using('second').create(browser=yekun.browser,os = yekun.os,device=yekun.device,useri=istifadeci_adi)
            if yoxla.status:
                return HttpResponseRedirect(reverse('dashboard'))
                
            else:
                return HttpResponseRedirect(reverse('activate'))
            messages.success(request,"Ugurla sisteme giris edildi ." ,extra_tags='success')
        else:
            messages.success(request,"Bu istifadeci movcud deyil . ",extra_tags='danger')
    context = {
        'form':form,
    }
    return render(request,'login.html',context)


def testCeleryi(request):
    data = request.META["HTTP_USER_AGENT"]
    ipaddress = request.META.get('REMOTE_ADDR')
    print(ipaddress)
    yekun = parse(data)
    print(yekun.browser,yekun.os,yekun.device)
    return HttpResponse("Done!")


@login_required(login_url=reverse_lazy('login'))
def activateprof(request):
    form = ActivationForm(request.POST or None)
    if form.is_valid():
        code    =  form.cleaned_data.get('code')
        codedb  =  activateProfile.objects.get(useri=request.user)  
        if int(code) == codedb.code:
            codedb.status = True
            print(codedb.status)
            codedb.save()
            messages.success(request,"Tebrikler, Hesabiniz tesdiqlendi. ",extra_tags="success")
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            messages.success(request,"Teessuf, Kod yanlisdir. ",extra_tags="danger")
            return HttpResponseRedirect(reverse('activate'))
    context = {
        'form':form,
    }
    return render(request,'activate.html',context)


@login_required(login_url=reverse_lazy('login'))
def dashboard(request):
    form    = TodoForm(request.POST or None)
    #todolar = todo.objects.filter(useri=request.user)
    paylasilan_todolar = todopaylas.objects.filter(alan_id = request.user,tesdiq=True).order_by("-id")
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
def logouting(request):
    try:
        logout(request)
        messages.success(request,"Sistemden ugurla cixis edildi.",extra_tags='success')
        return HttpResponseRedirect(reverse('register'))
    except:
        messages.success(request,"Sistemden cixis edilerken problem yaranda.",extra_tags='danger')
        return HttpResponseRedirect(reverse('dashboard'))


