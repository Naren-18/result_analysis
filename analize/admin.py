import django
from django.contrib import admin
from .models import Mydata,Reference,Login
admin.site.register(Mydata)
admin.site.register(Login)

admin.site.register(Reference)

# Register your models here.
