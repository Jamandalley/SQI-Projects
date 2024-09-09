from django import forms
from django.contrib.auth.models import User
from medical.userapp.models import Profile
from .models import *

class Service_form(forms.ModelForm):
    list_HOD = []
    for hod in Profile.objects.all().filter(position='HOD'):
        list_HOD.append((hod.user_id, hod.user.first_name + " " + hod.user.last_name + " (" + hod.department +")"))

    service_logo = forms.FileField(required=False)
    HoD = forms.ChoiceField(choices=list_HOD, required=True)
    description = forms.CharField(widget=forms.Textarea())
    class Meta:
        model = Services
        fields = [
            'service_option',
            'HoD',
            'service_logo',
            'price',
            'description'
        ]