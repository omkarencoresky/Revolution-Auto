"""
URL configuration for RevolutionAuto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from admin_app import admin_views, user_views
from admin_app import car_views, location_views, service_views, mechanic_views


urlpatterns = [
    
    # -------------------------------------Admin urls----------------------------- #

    path('dashboard/', admin_views.dashboard, name = 'admin_dashboard'), #name not include 
    # path('registration/', admin_views.registration, name = 'admin_registration'),
    path('admin-management/', admin_views.admin_data_handler, name = 'admin_data_handler'),
    path('admin-management/<int:id>/', admin_views.admin_action_handler, name = 'admin_action_handler'),

    # -------------------------------------Car Brand urls------------------------- #

    path('car-brand/', car_views.car_brand_data_handler, name = 'car_brand_data_handler'),
    path('car-brand/<int:id>/', car_views.car_brand_action_handler, name = 'car_brand_action_handler'),
    
    # -------------------------------------Car Year urls-------------------------- #

    path('car-year/', car_views.car_year_data_handler, name = 'car_year_data_handler'),
    path('car-year/<int:id>/', car_views.car_year_action_handler, name = 'car_year_action_handler'),

    # -------------------------------------Car model urls------------------------- #

    path('car-model/', car_views.car_model_data_handler, name = 'car_model_data_handler'),
    path('car-model/<int:id>/', car_views.car_model_action_handler, name = 'car_model_action_handler'),
    
    # -------------------------------------Car Trim url--------------------------- #

    path('car-trim/', car_views.car_trim_data_handler, name = 'car_trim_data_handler'),
    path('car-trim/<int:id>/', car_views.car_trim_action_handler, name = 'car_trim_action_handler'),    
    
    # -------------------------------------location urls-------------------------- #

    path('location/', location_views.location_data_handler, name = 'location_data_handler'),
    path('location/<int:id>/', location_views.location_action_handler, name = 'location_action_handler'),
    
    # -------------------------------------Serivice Type urls--------------------- #

    path('service-type/',service_views.service_type_data_handler, name = 'service_type_data_handler'),
    path('service-type/<int:id>/', service_views.service_type_action_handler, name = 'service_type_action_handler'),

    # -------------------------------------Serivice Category urls----------------- #

    path('service-category/',service_views.service_category_data_handler, name = 'service_category_data_handler'),
    path('service-category/<int:id>/', service_views.service_category_action_handler, name = 'service_category_action_handler'),

    # -------------------------------------Serivices urls------------------------- #

    path('service/', service_views.service_data_handler, name = 'service_data_handler'),
    path('service/<int:id>/', service_views.service_action_handler, name = 'service_action_handler'),

    # -------------------------------------Sub-serivices urls--------------------- #

    path('sub-service/', service_views.sub_services_data_handler, name = 'sub_services_data_handler'),
    path('sub-service/<int:id>/', service_views.sub_services_action_handler, name = 'sub_services_action_handler'),

    # -------------------------------------Sub-serivice option urls--------------------- #

    path('sub-service-option/', service_views.sub_service_option_data_handler, name = 'sub_service_option_data_handler'),
    path('sub-service-option/<int:id>/', service_views.sub_service_option_action_handler, name = 'sub_service_option_action_handler'),
       
     # -------------------------------------User management urls--------------------- #
    path('user-management/', user_views.user_data_handler, name = 'user_data_handler'),
    path('user-login-as-admin/<int:id>/', user_views.admin_login_as_user, name = 'admin_login_as_user'),
    path('user-management/<int:id>/<str:role>/', user_views.user_action_handler, name = 'user_action_handler'),

    # -------------------------------------Mechanic management urls--------------------- #

    path('mechanic-management/', mechanic_views.mechanic_data_handler, name = 'mechanic_data_handler'),
    path('mechanic-management/<int:id>/', mechanic_views.mechanic_action_handler, name = 'mechanic_action_handler'),
    

]


