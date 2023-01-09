
from django.urls import path,include
from . import views
from . import admin

urlpatterns = [
   path('',views.login,name='login'),
   path('logout',views.logout,name='logout'),

    path('index',views.index,name='index'),
    
    path('home',views.home,name='home'),
    path('retrive',views.retrive,name='retrive'),
    path('func',views.func),
    path('batch',views.batch,name='batch'),
    path('upload',views.upload,name='upload'),
    path('get',views.get,name='get'),
    path('analyize',views.analyize,name='analyize'),
    path('sem',views.sem,name='sem'),
    path('clear',views.clear,name="clear")
]
