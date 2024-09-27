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
from user_app import user_app_views, user_views

urlpatterns = [

    # --------------Basic and common urls--------------
    path('', user_app_views.index, name='Home'),
    path('team/', user_app_views.team, name='Team'),
    path('about/', user_app_views.about, name='About'),
    path('login/', user_app_views.login, name='login'),
    path('service/', user_app_views.service, name='Service'),
    path('booking/', user_app_views.booking, name='Booking'),
    path('logout/', user_app_views.logout_view, name='logout'),
    path('register/', user_app_views.register, name='register'),


    # -------------- User urls--------------
    path('user/dashboard', user_views.user_dashboard, name='user_dashboard'),
    path('user/<int:id>/', user_views.user_userapp_action_handler, name='user_userapp_action_handler'),

    
    path('users-car/', user_views.user_car_data_handler, name='user_car_data_handler'),
    path('users-car/<int:id>/', user_views.user_car_action_handler, name='user_car_action_handler'),


    # -------------- Add Car detail from options urls--------------
    path('get_caryear_options/', user_views.get_caryear_options, name='get_caryear_options'),
    path('get_cartrim_options/', user_views.get_cartrim_options, name='get_cartrim_options'),
    path('get_carmodel_options/', user_views.get_carmodel_options, name='get_carmodel_options'),


    # -------------- Referral based urls--------------
    path('user-referral/', user_views.referral_data_handler, name='referral_data_handler'),
]
