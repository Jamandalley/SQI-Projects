from django.urls import re_path
from medical.serviceapp import views as serv_views

urlpatterns = [
    re_path(r'^homepage_service/',serv_views.homepage_service,name='homepage_service'),
    re_path(r'^create_service/',serv_views.createService,name='create_service'),
    re_path(r'^display_service/',serv_views.displayService,name='display_service'),
    re_path(r'^edit_service/(?P<serv_id>\d+)/',serv_views.edit_service,name='edit_service'),
    re_path(r'^delete_service/(?P<serv_id>\d+)/',serv_views.deleteService,name='delete_service'),
    re_path(r'^view_service/(?P<serv_id>\d+)/',serv_views.viewService,name='view_service'),
]