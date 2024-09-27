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
from mechanic_app import views
urlpatterns = [
    # --------------Basic and common urls--------------
    path('', views.register_mechanic_application, name='register_mechanic_application'),
    path('dashboard/', views.mechanic_dashboard, name='mechanic_dashboard'),
    path('mechanic_dashboard/<int:id>/', views.mechanic_mechanicapp_data_controller, name='mechanic_mechanicapp_data_controller'),
]
