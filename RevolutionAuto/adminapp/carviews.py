import itertools
import os
import hashlib
from.models import CarBrand
from .forms import Addbrandform
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist

curl = settings.CURRENT_URL
admincurl = f"{curl}/adminapp/"
media_path = f'{settings.MEDIA_URL}car_brand_images/'   

def dashboard(request):
    """This method is use to render the dashboard page for Admin and show other different options.

    Args:
        request

    Returns:
        Httprequest: This method is use for render the Admin dashboard page.
    """
    return render(request, 'dashboard.html', {'curl':admincurl})

def car_brand(request):
    """This method is use to render the main page for car brand and show the brand's list

    Args:
        request

    Returns:
        Httprequest: This method is use for render the car brand page.
    """
    all_brands = CarBrand.objects.all()
    count=1
    return render(request, 'car_brand.html', {'curl':admincurl, 'brands':all_brands, 'count':count})

def add_brand(request):
    """This Method is allow to insert the another one brand of car itno the database. 

    Args:
        request

    Returns:
        Httprequest: Added the recored and if success redirect onthe same page and if fail render on same page
    """
    try:
        form = Addbrandform(request.POST, request.FILES)
        try:
            if form.is_valid():
                brand = form.save(commit=False)
                mod_name = request.POST['brand']
                token = hashlib.sha256(mod_name.encode()).hexdigest()
                uploaded_file = request.FILES['car_image']
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
                return redirect('car_brand', {'curl':admincurl})
            
            else:
                messages.error(request, 'Invalid request, Try again')
                return render ('car_brand.html', {'curl':admincurl}) 
            
        except Exception as e:
            messages.error(request, f"{e}")
            return render ('car_brand.html', {'curl':admincurl})
        
    except Exception as e:
        messages.error(request, f"{e}")
        return render ('car_brand.html', {'curl':admincurl})
    

def edit_brand(request):
    pass


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
        all_brands = CarBrand.objects.all()
        
        context = {
            'brands': all_brands
            # 'curl': request.build_absolute_uri('/'),
        }
        
        messages.success(request,f"{brand.brand} brand deleted successfully")
        return render(request, 'car_brand.html',context , status=200)
    
    except ObjectDoesNotExist:
        # Handle case where the object does not exist
        messages.error(f"CarBrand with id {id} does not exist.")
        return HttpResponse("Brand not found.", status=404)
    
    except Exception as e:  
        messages.error(f"Error: {str(e)}")
        return render(request, 'car_brand.html', status=500)