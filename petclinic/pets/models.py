from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.user.username

class Pet(models.Model):
    name = models.CharField(max_length=50)
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    age = models.IntegerField()
    owner = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.species})"
    

class Appointment(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='appointments')
    owner = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Completed', 'Completed')], default='Pending')

    def __str__(self):
        return f"Appointment for {self.pet.name} on {self.date}"

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='articles')

    def __str__(self):
        return self.title

class MedicalRecord(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='medical_records')
    owner = models.ForeignKey(Client, on_delete=models.CASCADE)
    visit_date = models.DateField()
    notes = models.TextField()
    treatments = models.TextField()

    def __str__(self):
        return f"Medical Record for {self.pet.name} on {self.visit_date}"