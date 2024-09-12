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
from user_app import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='Home'),
    path('team/', views.team, name='Team'),
    path('about/', views.about, name='About'),
    path('login/', views.login, name="login"),
    path('service/', views.service, name='Service'),
    path('booking/', views.booking, name='Booking'),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name='register'),
]
