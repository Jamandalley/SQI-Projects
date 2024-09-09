from django.urls import re_path
from medical.appointmentapp import views as appt_views

urlpatterns = [
    re_path(r'^display_appointment/',appt_views.display_appointment,name='display_appointment'),
    re_path(r'^create_appointment/(?P<userid>\d+)/',appt_views.create_appointment,name='create_appointment'),
    re_path(r'^edit_appointment/(?P<appt_id>\d+)/',appt_views.edit_appointment,name='edit_appointment'),
    re_path(r'^delete_appointment/(?P<appt_id>\d+)/',appt_views.deleteAppointment,name='delete_appointment')

]