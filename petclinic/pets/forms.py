from django import forms
from .models import Client, Pet, Appointment, Article, MedicalRecord
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):

    pass


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['user', 'phone_number', 'address']

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'breed', 'age', 'owner']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['pet', 'date', 'reason', 'status']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'author']

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['pet', 'visit_date', 'notes', 'treatments']