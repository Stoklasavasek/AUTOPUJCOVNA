
from django.contrib import admin
from .models import Zakaznik, Auto, Pujcka, Platba, Servis

admin.site.register(Zakaznik)
admin.site.register(Auto)
admin.site.register(Pujcka)
admin.site.register(Platba)
admin.site.register(Servis)
