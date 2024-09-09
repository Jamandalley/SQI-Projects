from django import forms
from django.contrib.auth.models import User
from medical.userapp.models import Profile
from .models import *

class Appointment_form(forms.ModelForm):
    
    class Meta:
        model = Book_appointment
        fields = [
            'department',
            'appointment_time',
            'appointment_date',
        ]
        widgets = {
            'appointment_time': forms.NumberInput(attrs={'type':'time'}),
            'appointment_date': forms.NumberInput(attrs={'type':'date'}),
        }
        
class Edit_appointment_form(forms.ModelForm):
    
    class Meta:
        model = Book_appointment
        fields = [
            'department',
            'appointment_time',
            'appointment_date',
            'approved_date',
            'approved_time',
            'status'

        ]
        widgets = {
            'appointment_time': forms.NumberInput(attrs={'type':'time'}),
            'appointment_date': forms.NumberInput(attrs={'type':'date'}),
            'approved_time': forms.NumberInput(attrs={'type':'time'}),
            'approved_date': forms.NumberInput(attrs={'type':'date'}),
        }
        

    # doctors = forms.ModelChoiceField(
    # queryset=Profile.objects.all().filter(position='Consultant'), 
    # label='Select a Doctor',
    # )
