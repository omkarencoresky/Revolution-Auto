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
from adminapp import carviews, location_views
from django.urls import path


urlpatterns = [
    
    # Admin urls
    path('dashboard/', views.dashboard, name='admin_dashboard'), #name not include 
    path('registration/', views.registration, name='admin_registration'),

    # Car Brand urls
    path('car/brands/', carviews.all_car_brands, name='all_car_brands'),
    path('add/car/brand/', carviews.add_car_brand, name='add_car_brand'),
    path('add/brand/page/', carviews.display_add_brand, name='add_brand_page'),
    path('update/brand/<int:id>/', carviews.update_car_brand, name='update_car_brand'),
    path('delete/car/brand/<int:id>/', carviews.delete_car_brand, name='delete_car_brand'),
    
    # Car Year urls
    path('car/years/', carviews.all_car_years, name='all_car_years'),
    path('add/car/year/', carviews.add_car_year, name='add_car_year'),
    path('add/year/page/', carviews.display_add_year, name='add_year_page'),
    path('update/car/year/<int:id>/', carviews.update_car_year, name='update_car_year'),
    path('delete/car/year/<int:id>/', carviews.delete_car_year, name='delete_car_year'),

    # Car model urls
    path('car/models/', carviews.all_car_models, name='all_car_models'),
    path('add/car/model/', carviews.add_car_model, name='add_car_model'),   
    path('add/model/page/', carviews.display_add_model, name='add_model_page'),
    path('update/car/model/<int:id>/', carviews.update_car_model, name='update_car_model'),
    path('delete/car/model/<int:id>/', carviews.delete_car_model, name='delete_car_model'),

    # Car Trim url
    path('car/trims/', carviews.all_car_trims, name='all_car_trims'),
    path('add/car/trim/', carviews.add_car_trim, name='add_car_trim'),
    path('add/trim/page/', carviews.display_add_trim, name='add_trim_page'),
    path('update/car/trim/<int:id>/', carviews.update_car_trim, name='update_car_trim'),
    path('delete/car/trim/<int:id>/', carviews.delete_car_trim, name='delete_car_trim'),

    # location urls
    path('add/location/', location_views.add_location, name='add_location'),
    path('get/locations/', location_views.all_location, name='get_all_locations'),
    path('delete/location/<int:id>/', location_views.delete_location, name='delete_location'),
    path('update/location/<int:id>/', location_views.update_location, name="update_location"),
    path('add/location/page/', location_views.display_add_location, name='display_location_page'),
]


