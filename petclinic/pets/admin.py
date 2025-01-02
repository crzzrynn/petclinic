from django.contrib import admin
from .models import Client, Pet, Appointment, MedicalRecord, Article

# Register your models here.

admin.site.register(Client)
admin.site.register(Pet)
admin.site.register(Appointment)
admin.site.register(MedicalRecord)
admin.site.register(Article)