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
from adminapp import carviews
from django.urls import path

urlpatterns = [
    path('registration/', views.registration),
    path('dashboard/', views.dashboard),
    path('carbrand/', carviews.car_brand, name='car_brand'),
    path('addbrand/', carviews.add_brand),
    path('showaddbrand/', carviews.ShowAddBrand),
    path('deletebrand/<int:id>/', carviews.delete_brand, name='deleteBrand'),
    path('editbrand/<int:id>/', carviews.edit_brand, name='editbrand'),
]
