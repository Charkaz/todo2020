from django.urls import path,include
from start.views import dashboard
from .views import yeniTodo,tododetail,todoUpdate,paylas,isteksil,istekqebul,axtaris,room,serhsil
from .views import serhupdate

urlpatterns = [
    path('',dashboard,name="dashboard"),
    path('todoqeyd',yeniTodo,name='todoqeyd'),
    path('tododetail/<str:id>',tododetail,name='tododetail'),
    path('todoupdate/<str:id>',todoUpdate,name='todoupdate'),
    path('paylas/<str:id>',paylas,name = 'paylas'),
    path('isteksil/<str:id>',isteksil,name ='isteksil'),
    path('istekqebul/<str:id>',istekqebul,name='istekqebul'),
    path('axtaris',axtaris,name = 'axtaris'),
    path('tododetailserh/<str:room_name>/', room, name='room'),
    path('seerhsil/<str:id>',serhsil,name = 'serhsil'),
    path('serhupdate/<str:id>',serhupdate,name='serhupdate'),
]
