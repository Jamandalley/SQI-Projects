from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Book_appointment(models.Model):
    dept = [
        ("Emergency", "Emergency"),
        ("Operation & Surgery", "Operation & Surgery"),
        ("Outdoor Checkup", "Outdoor Checkup"),
        ("Ambulance Service", "Ambulance Service"),
        ("Medicine & Pharmacy", "Medicine & Pharmacy"),
        ("Medical Lab","Medical Lab")
    ]

    status = [
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Declined', 'Declined')
    ]


    appointment_id = models.AutoField(primary_key=True)
    department = models.CharField(choices=dept, null=True, blank=True, unique=False, max_length= 20)
    appointment_date = models.DateField(null=True, blank=True, unique=False)
    doctor_incharge = models.ForeignKey(User, related_name="Doctor_incharge", null=False, blank=False, unique=False, on_delete=models.CASCADE, default=1)
    appointment_time = models.TimeField(null=True, blank=True, unique=False)
    client_name = models.CharField(max_length=20, null=True, blank=True, unique=False)
    client_email = models.CharField(max_length=20, null=True, blank=True, unique=False)
    approved_date = models.DateField(null=True, blank=True, unique=False)
    approved_time = models.TimeField(null=True, blank=True, unique=False)
    status = models.CharField(max_length=20, choices=status, null=False, blank=False, unique=False, default='Pending')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'APT0{self.appointment_id}-{self.client_name}'