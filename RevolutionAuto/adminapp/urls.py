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
    
    # Admin urls
    path('dashboard/', views.dashboard),
    path('registration/', views.registration),

    # Car Brand urls
    path('addbrand/', carviews.add_brand),
    path('showaddbrand/', carviews.show_add_brand),
    path('carbrand/', carviews.car_brand, name='carbrand'),
    path('editbrand/<int:id>/', carviews.edit_brand, name='editbrand'),
    path('deletebrand/<int:id>/', carviews.delete_brand, name='deleteBrand'),
    
    # Car Year urls
    path('caryear/', carviews.car_year, name='caryear'),
    path('addyear/', carviews.add_year, name='add_year'),
    path('edityear/<int:id>/', carviews.edit_year, name='edityear'),
    path('showaddyear/', carviews.show_add_year, name='showaddyear'),
    path('deleteyear/<int:id>',carviews.delete_year, name='deleteYear'),

    # Car model urls
    path('carmodel/', carviews.car_model, name='carmodel'),
    path('addmodel/', carviews.add_model, name='addmodel'),
    path('editmodel/<int:id>/', carviews.edit_model, name='editmodel'),
    path('showaddmodel/', carviews.show_add_model, name='showaddmodel'),
    path('deletemodel/<int:id>/', carviews.delete_model, name='deletemodel'),

    # Car Trim url
    path('cartrim/', carviews.car_trim, name='cartrim'),
    path('addtrim/', carviews.add_trim, name='addtrim'),
    path('edittrim/<int:id>/', carviews.edit_trim, name='edittrim'),
    path('showaddtrim/', carviews.show_add_trim, name='showaddtrim'),
    path('deletetrim/<int:id>/', carviews.delete_trim, name='deletetrim'),
]


