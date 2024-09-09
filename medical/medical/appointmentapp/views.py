from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from medical.userapp.models import Profile
from django.contrib.auth.models import User
from .forms import *
from .models import *
from django.contrib import messages
from django.http import HttpResponsePermanentRedirect
from django.db.models import Q
from django.core.mail import send_mail


@login_required
def display_appointment(request):
    
    if request.user.is_superuser:
        appointment = Book_appointment.objects.all()
    elif request.user.is_staff:
        doctor = Profile.objects.get(user_id = request.user.id)
        appointment = Book_appointment.objects.all().filter(department = doctor.department)
    else:
        client = User.objects.get(id = request.user.id)
        client_name = client.first_name +' '+ client.last_name
        appointment = Book_appointment.objects.all().filter(client_name = client_name)
        print(request.user.email)

    return render(request, template_name='appointmentapp/display_appointment.html', context={'appointments':appointment})

@login_required
def create_appointment(request, userid):
    if request.method == "POST":
        appt_form = Appointment_form(request.POST)
        client = User.objects.get(id = userid)
        department = request.POST.get('department', None)
        print(department)
        if appt_form.is_valid():
            form = appt_form.save(commit=False)
            form.client_name = client.first_name +' '+ client.last_name
            form.client_email = client.email
            try:
                doctor_incharge = Profile.objects.get(Q(position = 'HOD') & Q(department = department) )
                doctor_incharge = User.objects.get(id = doctor_incharge.user_id)
                form.doctor_incharge = doctor_incharge
                
            except:
                doctor_incharge = Profile.objects.get(position = 'CMD')
                doctor_incharge = User.objects.get(id = doctor_incharge.user_id)
                form.doctor_incharge = doctor_incharge

            form.save()
            messages.success(request, 'Appointment Booked Successfully')

            send_mail(
            'Booking has been made by a patient',# Subject of the mail
            f'Dear Dr. {doctor_incharge.first_name}, a patient has booked a service. Please do a proper follow up ', # Body of the mail
            'medical@gmail.com', # From email (Sender)
            [doctor_incharge.email], # To email (Receiver)
            fail_silently=False, # Handle any error
            )


            send_mail(
            'Booking has been made by a patient',# Subject of the mail
            f'Dear Sir/Ma {client.first_name}, Your appointment has been recieved.', # Body of the mail
            'medical@gmail.com', # From email (Sender)
            [client.email], # To email (Receiver)
            fail_silently=False, # Handle any error
            )

            return display_appointment(request)
        else:
            messages.error(request, 'Booking not successfull, Retry')
            return redirect('create_appointment')
        
    else:
        appt_form = Appointment_form()

        return render(request, 'appointmentapp/create_appointment.html', {'appt_form': appt_form})
    


@login_required
def edit_appointment(request, appt_id):
    appointment = get_object_or_404(Book_appointment, appointment_id=appt_id)
    
    if request.method == "POST":
        if request.user.is_staff:
            appt_form = Edit_appointment_form(request.POST, instance=appointment)
        else:
            appt_form = Appointment_form(request.POST, instance=appointment)
        
        if  appt_form.is_valid():
            appt_form.save()
           
            messages.success(request, 'Appointment successfully updated!')
            return display_appointment(request)
        else:
        #     print("invalid invalid")
            messages.error(request, 'Please correct the error below.')
            return HttpResponsePermanentRedirect(reverse('editAppointment', args=(appt_id,)))
    else:
        if request.user.is_staff:
            appt_form = Edit_appointment_form(instance=appointment)
        else:
            appt_form = Appointment_form(instance=appointment)
        return render(request, 'appointmentapp/edit_appointment.html', {'appt_form': appt_form})


@login_required
def deleteAppointment(request, appt_id):
    try:
        Book_appointment.objects.get(appointment_id = appt_id).delete()
        messages.info(request, 'Appointment deleted successfully')
    except:
        messages.error(request, 'Something went wrong')
        return HttpResponsePermanentRedirect(reverse('editAppointment', args=(appt_id,)))

    return redirect('display_appointment')

