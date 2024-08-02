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
from django.urls import path, include
from super_adminapp import views

urlpatterns = [
    path('home/',views.index, name='Home'),
    path('error/', views.error, name='error'),
    path('about/',views.about, name='About'),
    path('service/',views.service, name='Service'),
    path('team/',views.team, name='Team'),
    path('booking/',views.booking, name='Booking'),
    path('register/', views.register, name="register")
]