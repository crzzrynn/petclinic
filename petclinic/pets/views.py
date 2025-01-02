from django.shortcuts import render, redirect, get_object_or_404
from .models import Client, Pet, Appointment, Article, MedicalRecord
from .forms import ClientForm, PetForm, AppointmentForm, ArticleForm, MedicalRecordForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import CustomAuthenticationForm
import logging

logger = logging.getLogger(__name__)
class CustomLoginView(LoginView):
    template_name = 'pets/login.html'  
    authentication_form = CustomAuthenticationForm

    def post(self, request, *args, **kwargs):
        logger.debug("Request data: %s", request.POST) 
        return super().post(request, *args, **kwargs)
    
def logout_view(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            messages.success(request, 'Registration successful!')
            return redirect('login')  
    else:
        form = UserCreationForm()
    return render(request, 'pets/register.html', {'form': form})

@login_required
def home(request):
    return render(request, 'pets/base.html')


# Client Views
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'pets/client_list.html', {'clients': clients})

def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'pets/client_form.html', {'form': form})

def edit_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'pets/client_form.html', {'form': form})

def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    return render(request, 'pets/client_confirm_delete.html', {'client': client})

# Pet Views
@login_required
def pet_list(request):
    if request.user.is_staff:  
        pets = Pet.objects.all() 
    else:  
        client = get_object_or_404(Client, user=request.user)
        pets = Pet.objects.filter(owner=client)  
    return render(request, 'pets/pet_list.html', {'pets': pets})

@login_required
def create_pet(request):
    if request.user.is_staff:  
        form = PetForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('pets:pet_list')
    else:
        client = get_object_or_404(Client, user=request.user)  
        form = PetForm(request.POST or None)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = client  
            pet.save()
            return redirect('pets:pet_list')
    return render(request, 'pets/pet_form.html', {'form': form})

@login_required
def edit_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.user.is_staff or pet.owner == Client.objects.get(user=request.user):  
        form = PetForm(request.POST or None, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('pets:pet_list')
    else:
        return render(request, 'pets/error.html', {'message': 'You do not have permission to edit this pet.'})
    return render(request, 'pets/pet_form.html', {'form': form, 'pet': pet})  

@login_required
def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)  
    client = get_object_or_404(Client, user=request.user)  

    if pet.owner != client:  
        return render(request, 'pets/error.html', {'message': 'You do not have permission to delete this pet.'})

    if request.method == 'POST':
        pet.delete()  
        return redirect('pets:pet_list')  

    return render(request, 'pets/pet_confirm_delete.html', {'pet': pet}) 
# Appointment Views
@login_required
def appointment_list(request):
    if request.user.is_staff:  
        appointments = Appointment.objects.all()  
    else:  
        client = get_object_or_404(Client, user=request.user)
        appointments = Appointment.objects.filter(owner=client) 
    return render(request, 'pets/appointment_list.html', {'appointments': appointments})

def create_appointment(request):
    
    client = get_object_or_404(Client, user=request.user)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)  
        if form.is_valid():
            appointment = form.save(commit=False)  
            appointment.owner = client  
            appointment.save()  
            return redirect('pets:appointment_list')  
    else:
        form = AppointmentForm()  

    return render(request, 'pets/appointment_form.html', {'form': form})  

@login_required
def edit_appointment(request, appointment_id):
   
    appointment = get_object_or_404(Appointment, id=appointment_id)
    client = get_object_or_404(Client, user=request.user)

    if appointment.owner != client:
        return redirect('pets:appointment_list')

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment) 
        if form.is_valid():
            form.save()  
            return redirect('pets:appointment_list')  
    else:
        form = AppointmentForm(instance=appointment)  

    return render(request, 'pets/appointment_form.html', {'form': form, 'appointment': appointment})  #
@login_required
def delete_appointment(request, appointment_id):

    appointment = get_object_or_404(Appointment, id=appointment_id)
    client = get_object_or_404(Client, user=request.user)


    if appointment.owner != client:
        return redirect('pets:appointment_list')  

    if request.method == 'POST':
        appointment.delete() 
        return redirect('pets:appointment_list')  

    return render(request, 'pets/appointment_confirm_delete.html', {'appointment': appointment}) 


def article_list(request):
    articles = Article.objects.all()
    return render(request, 'pets/article_list.html', {'articles': articles})

@login_required
def create_article(request):
    if not request.user.is_staff:
        return render(request, 'pets/error.html', {'message': 'You do not have permission to create articles.'})
    form = ArticleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('article_list')
    return render(request, 'pets/article_form.html', {'form': form})

@login_required
def edit_article(request, article_id):
    if not request.user.is_staff:
        return render(request, 'pets/error.html', {'message': 'You do not have permission to edit articles.'})
    article = get_object_or_404(Article, id=article_id)
    form = ArticleForm(request.POST or None, instance=article)
    if form.is_valid():
        form.save()
        return redirect('article_list')
    return render(request, 'pets/article_form.html', {'form': form})

@login_required
def delete_article(request, article_id):
    if not request.user.is_staff:
        return render(request, 'pets/error.html', {'message': 'You do not have permission to delete articles.'})
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        article.delete()
        return redirect('article_list')
    return render(request, 'pets/article_confirm_delete.html', {'article': article})

# Medical Record Views
@login_required
def medical_record_list(request):
    if request.user.is_staff:  
        records = MedicalRecord.objects.all()  
    else: 
        client = get_object_or_404(Client, user=request.user)
        records = MedicalRecord.objects.filter(owner=client)  
    return render(request, 'pets/medical_record_list.html', {'records': records})


@login_required
def create_medical_record(request):
    client = get_object_or_404(Client, user=request.user) 
    form = MedicalRecordForm()  

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)  
        if form.is_valid():
            medical_record = form.save(commit=False)  
            medical_record.owner = client  
            medical_record.save()  
            return redirect('pets:medical_record_list')  
        else:
            print(form.errors)  

    return render(request, 'pets/medical_record_form.html', {'form': form})  

@login_required
def edit_medical_record(request, record_id):
    medical_record = get_object_or_404(MedicalRecord, id=record_id, owner=request.user) 
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, instance=medical_record)
        if form.is_valid():
            form.save()
            return redirect('medical_record_list')
    else:
        form = MedicalRecordForm(instance=medical_record)
    return render(request, 'pets/medical_record_form.html', {'form': form})

@login_required
def delete_medical_record(request, record_id):
    medical_record = get_object_or_404(MedicalRecord, id=record_id, owner=request.user)  
    if request.method == 'POST':
        medical_record.delete()
        return redirect('medical_record_list')
    return render(request, 'pets/medical_record_confirm_delete.html', {'medical_record': medical_record})

