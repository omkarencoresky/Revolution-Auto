import itertools
import json
import os
import hashlib
from.models import CarBrand
from .forms import Addbrandform
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

curl = settings.CURRENT_URL
admincurl = f"{curl}/adminapp"
media_path = f'{settings.MEDIA_URL}'   

def pagination(request):
    all_brands = CarBrand.objects.all()
    
    # Pagination setup
    paginator = Paginator(all_brands, 10)  # Show 10 brands per page
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)  # Get the page object for the requested page
    return page_obj

def dashboard(request):
    """This method is use to render the dashboard page for Admin and show other different options.

    Args:
        request

    Returns:
        Httprequest: This method is use for render the Admin dashboard page.
    """
    page_obj = pagination(request)

    context = {
        'page_obj': page_obj,
        'curl':admincurl
    }
    return render(request, 'dashboard.html', context)

def car_brand(request):
    """This method is use to render the main page for car brand and show the brand's list

    Args:
        request

    Returns:
        Httprequest: This method is use for render the car brand page.
    """
    page_obj = pagination(request)

    context = {
        'page_obj': page_obj,
        'curl':admincurl
    }

    return render(request, 'car_brand.html', context)

def add_brand(request):
    """This Method is allow to insert the another one brand of car itno the database. 

    Args:
        request

    Returns:
        Httprequest: Added the recored and if success redirect onthe same page and if fail render on same page
    """
    try:
        if request.method == 'POST':
            form = Addbrandform(request.POST, request.FILES)
            page_obj = pagination(request)
            count=1

            context = {
                'page_obj': page_obj,
                'curl':admincurl,
                'count':count
            }
            try:
                if form.is_valid():
                    brand = form.save(commit=False)
                    brand_name = request.POST['brand']
                    token = hashlib.sha256(brand_name.encode()).hexdigest()
                    uploaded_file = request.FILES['image_url']
                    image_name = uploaded_file.name
                    brand.image_url = f"{media_path}{image_name}"   
                    brand.remember_token = token
                    media_directory = os.path.join(settings.BASE_DIR, 'media')
                    file_path = os.path.join(media_directory, image_name)

                    if not os.path.exists(media_directory):
                        os.makedirs(media_directory)

                    with open(file_path, "wb") as fp:
                        for chunk in uploaded_file.chunks():
                            fp.write(chunk)
                    form.save()
                    messages.success(request, "One more car brand has been added successfully!")
                    return render(request, 'car_brand.html', context)
                
                else:
                    messages.error(request, 'Invalid request, Try again')
                    return render (request, 'car_brand.html', context) 
                
            except Exception as e:
                messages.error(request, f"{e}")
                return render (request, 'car_brand.html', context)
        
    except Exception as e:
        messages.error(request, f"{e}")
        return render (request, 'car_brand.html', context)


def ShowAddBrand(request):
    return render(request, 'showaddbrand.html', {'curl':admincurl})

@csrf_exempt # It is used for avoid admin login 
def delete_brand(request, id):
    """This method is allow to Delete brand record with the confirmation popup

    Args:
        request (_type_): _description_
        id (integer): Thi is brand record id 

    Returns:
        Httprequest: if the brand id is available the render it on the car_brand page withh success 
        message and if not than shoe the error on same page.
    """

    try:
        brand = CarBrand.objects.get(id=id)
        brand.delete()
        page_obj = pagination(request)
        
        context = {
            'page_obj': page_obj,
            'curl': request.build_absolute_uri(admincurl)
        }
        
        messages.success(request,f"{brand.brand} brand deleted successfully")
        return render(request, 'car_brand.html',context , status=200)
    
    except ObjectDoesNotExist:
        # Handle case where the object does not exist
        messages.error(f"CarBrand with id {id} does not exist.")
        return render(request, 'car_brand.html', context, status=404)
    
    except Exception as e:  
        messages.error(f"Error: {str(e)}")
        return render(request, 'car_brand.html', context, status=500)
    

@csrf_exempt
def edit_brand(request, id):
    if request.method == 'GET':
        page_obj = pagination(request)
        context = {
                'page_obj': page_obj,
                'curl':admincurl,
            }
        brand = CarBrand.objects.get(id=id)
        return render(request, 'edit.html', context)
    
   
    try:
        page_obj = pagination(request)
        context = {
                'page_obj': page_obj,
                'curl':admincurl,
            }
        if request.method == 'POST':
            brand = CarBrand.objects.get(id=id)
            # brand.brand = request.POST.get('brand')
            old_make_name = brand.brand
            old_description = brand.description
            old_image_url = brand.image_url
            old_status = brand.status

            # For Brand name
            if request.POST.get('brand') == '':
                brand.brand = old_make_name
            else:
                brand.brand = request.POST['brand']
            
            # For Description name
            if request.POST.get('description') == '':
                brand.description = old_description
            else:
                brand.description = request.POST['description']
            
            # For status name
            if request.POST.get('status') == 1:
                brand.description = old_status
            else:
                brand.status = request.POST['status']
                
            # For image_url name
            if request.POST.get('image_url') == '':
                brand.image_url = old_image_url
            else:
                uploaded_file = request.FILES['image_url']
                image_name = uploaded_file.name
                brand.image_url = f"{media_path}{image_name}"
                media_directory = os.path.join(settings.BASE_DIR, 'media')
                file_path = os.path.join(media_directory, image_name)

                if not os.path.exists(media_directory):
                    os.makedirs(media_directory)

                with open(file_path, "wb") as fp:
                    for chunk in uploaded_file.chunks():
                        fp.write(chunk)
            brand.remember_token = brand.remember_token
            brand.save()
            messages.success(request, 'Brand is updated successfully!')
            return render(request, 'car_brand.html', context)
        else:
            messages.error(request, 'Invalid inputs, try again')
            return render(request, 'car_brand.html', context)

    except Exception as e:
        messages.error(request, f"{e}")
        return render(request, 'car_brand.html', context)

