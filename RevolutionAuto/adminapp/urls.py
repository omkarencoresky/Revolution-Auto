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

from adminapp import views  
from django.urls import path
from adminapp import carviews, location_views, serviceviews


urlpatterns = [
    
    # -------------------------------------Admin urls----------------------------- #

    path('dashboard/', views.dashboard, name='admin_dashboard'), #name not include 
    path('registration/', views.registration, name='admin_registration'),

    # -------------------------------------Car Brand urls------------------------- #

    path('car-brand/', carviews.car_brand_data_handler, name='car_brand_data_handler'),
    path('car-brand/<int:id>/', carviews.car_brand_action_handler, name='car_brand_action_handler'),
    
    # -------------------------------------Car Year urls-------------------------- #

    path('car-year/', carviews.car_year_data_handler, name='car_year_data_handler'),
    path('car-year/<int:id>/', carviews.car_year_action_handler, name='car_year_action_handler'),

    # -------------------------------------Car model urls------------------------- #

    path('car-model/', carviews.car_model_data_handler, name='car_model_data_handler'),
    path('car-model/<int:id>/', carviews.car_model_action_handler, name='car_model_action_handler'),
    
    # -------------------------------------Car Trim url--------------------------- #

    path('car-trim/', carviews.car_trim_data_handler, name='car_trim_data_handler'),
    path('car-trim/<int:id>/', carviews.car_trim_action_handler, name='car_trim_action_handler'),    
    
    # -------------------------------------location urls-------------------------- #

    path('location/', location_views.location_data_handler, name='location_data_handler'),
    path('location/<int:id>/', location_views.location_action_handler, name='location_action_handler'),
    
    # -------------------------------------Serivice Type urls--------------------- #

    path('service-type/',serviceviews.service_type_data_handler, name='service_type_data_handler'),
    path('service-type/<int:id>/', serviceviews.service_type_action_handler, name='service_type_action_handler'),

    # -------------------------------------Serivice Category urls----------------- #

    path('service-category/',serviceviews.service_category_data_handler, name='service_category_data_handler'),
    path('service-category/<int:id>/', serviceviews.service_category_action_handler, name='service_category_action_handler'),

    # -------------------------------------Serivices urls------------------------- #

    path('service/', serviceviews.service_data_handler, name='service_data_handler'),
    path('service/<int:id>/', serviceviews.service_action_handler, name='service_action_handler'),

    # -------------------------------------Sub-serivices urls--------------------- #

    path('sub-service/', serviceviews.sub_services_data_handler, name='sub_services_data_handler'),
    path('sub-service/<int:id>', serviceviews.sub_services_action_handler, name='sub_services_action_handler'),
       
]


