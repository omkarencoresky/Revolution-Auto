import os
import json
import hashlib
import schemas
import itertools
import fastjsonschema
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

import schemas.car_management_schemas
from .models import CarBrand, CarYear, CarModel, CarTrim
from .forms import Addbrandform, Addyearform, Addmodelform, Addtrimform
from schemas.car_management_schemas import validate_car_brand, validate_car_model, validate_car_trim, validate_car_year
from adminapp.utils.utils import brand_pagination, year_pagination, model_pagination, trim_pagination

curl = settings.CURRENT_URL
admincurl = f"{curl}/adminapp"
media_path = f'{settings.MEDIA_URL}'   


# Function for the brand model

def car_brand(request):
    """This method is use to render the main page for car brand and show the brand's list

    Args:
        request

    Returns:
        Httprequest: This method is use for render the car brand page.
    """
    page_obj = brand_pagination(request)

    context = {
        'page_obj': page_obj,
        'curl':admincurl
    }

    return render(request, 'carmodel/car_brand.html', context)

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
            page_obj = brand_pagination(request)
            count=1

            context = {
                'page_obj': page_obj,
                'curl':admincurl,
                'count':count
            }
            try:
                if not request.FILES.get('image_url'):
                    messages.success(request, "No image file selected. Please upload an image.")
                    return render(request, 'carmodel/car_brand.html', context)
                uploaded_file = request.FILES['image_url']
                image_name = uploaded_file.name 
                image_format = image_name.split('.')[-1].lower()

                data = {
                    'brand':request.POST.get('brand'),
                    'description':request.POST.get('description'),
                    'image_format':image_format
                }
                validate_car_brand(data)
                if form.is_valid():
                    brand = form.save(commit=False)
                    brand_name = request.POST['brand']
                    token = hashlib.sha256(brand_name.encode()).hexdigest()
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

                    page_obj = brand_pagination(request)
                    count=1

                    context = {
                        'page_obj': page_obj,
                        'curl':admincurl,
                        'count':count
                    }
                    messages.success(request, "One more car brand has been added successfully!")
                    return render(request, 'carmodel/car_brand.html', context)
                
                else:
                    messages.error(request, 'Invalid inputs in this form, Try again')
                    return render (request, 'carmodel/car_brand.html', context) 
                
            except fastjsonschema.exceptions.JsonSchemaValueException as e:
                messages.error(request,schemas.car_management_schemas.car_brand_schema.
                get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
                return render(request, 'car_brand.html', {'form': Addbrandform()}, status=400)
            except json.JSONDecodeError:
                messages.error(request, f"{e}")
                return render(request, 'car_brand.html', {'form': Addbrandform()}, status=400)
            
            except Exception as e:
                messages.error(request, f"Invalid input of this field {e}" )
                return render (request, 'carmodel/car_brand.html', context)
        
    except Exception as e:
        return render (request, 'carmodel/car_brand.html', context)

def show_add_brand(request):
    """This Method is allow to show the add brand page withe help of htmx request. 

    Args:
        request

    Returns:
        Httprequest: If success render the page page for add brands if fail render car brand or main.
    """
    return render(request, 'carmodel/showaddbrand.html', {'curl':admincurl})

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
    page_obj = brand_pagination(request)
        
    context = {
        'page_obj': page_obj,
        'curl': request.build_absolute_uri(admincurl)
    }
    try:
        brand = CarBrand.objects.get(id=id)
        brand.delete()
        page_obj = brand_pagination(request)
        
        context = {
            'page_obj': page_obj,
            'curl': request.build_absolute_uri(admincurl)
        }
        
        messages.success(request,f"{brand.brand} brand deleted successfully")
        return render(request, 'carmodel/car_brand.html',context , status=200)
    
    except ObjectDoesNotExist:
        # Handle case where the object does not exist
        messages.error(request, f"CarBrand with id {id} does not exist.")
        return render(request, 'carmodel/car_brand.html', context, status=404)
    
    except Exception as e:  
        messages.error(f"Error: {str(e)}")
        return render(request, 'carmodel/car_brand.html', context, status=500) 

@csrf_exempt # It is used for avoid admin login 
def edit_brand(request, id):
    """
    Updates the details of a car brand based on the provided form data.
    
    Args:
    - request (HttpRequest): The incoming HTTP request containing the form data for updating the brand.
    - id (int): The unique identifier of the car brand to be updated.
    
    Returns:
    - HttpResponseRedirect: Redirects to the main car brand listing page if the update is successful.
    - HttpResponse: Renders the update form template with the submitted data and validation errors if the update fails.
    """
    try:
        if request.method == 'GET':
                brand = CarBrand.objects.get(id=id)
                context = {
                    'page_obj': brand_pagination(request),
                    'curl': admincurl,
                    'brand': brand,
                }
                return render(request, 'carmodel/brand_edit.html', context)

        if request.method == 'POST':
            brand = CarBrand.objects.get(id=id)
            context = {
            'page_obj': brand_pagination(request),
            'curl': admincurl,
            'brand': brand,
            }
            try:
                if not request.FILES.get('image_url'):
                    image_name = str(brand.image_url).split('/')[-1]
                    image_format = image_name.split('.')[-1].lower()
                else:
                    uploaded_file = request.FILES['image_url']
                    image_name = uploaded_file.name 
                    image_format = image_name.split('.')[-1].lower()
                data = {
                    'brand':request.POST.get('brand'),
                    'description':request.POST.get('description'),
                    'image_format':image_format
                }
                validate_car_brand(data)
                brand = CarBrand.objects.get(id=id)

                # Update fields with form data or keep old values
                brand.brand = request.POST.get('brand', brand.brand)
                brand.description = request.POST.get('description', brand.description)
                brand.status = request.POST.get('status', brand.status)

                # Handle image file upload
                uploaded_file = request.FILES.get('image_url')
                if uploaded_file:
                    image_name = uploaded_file.name
                    media_directory = os.path.join(settings.BASE_DIR, 'media')
                    file_path = os.path.join(media_directory, image_name)

                    if not os.path.exists(media_directory):
                        os.makedirs(media_directory)

                    with open(file_path, 'wb') as fp:
                        for chunk in uploaded_file.chunks():
                            fp.write(chunk)

                    brand.image_url = f"{settings.MEDIA_URL}{image_name}"

                brand.save()
                messages.success(request, 'Brand is updated successfully!')
                return redirect('carbrand')
            except fastjsonschema.exceptions.JsonSchemaValueException as e:
                    messages.error(request,schemas.car_management_schemas.car_brand_schema.
                    get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
                    return render(request, 'car_brand.html', {'form': Addbrandform()}, status=400)
            except json.JSONDecodeError:
                messages.error(request, f"{e}")
                return render(request, 'car_brand.html', {'form': Addbrandform()}, status=400)
            except ObjectDoesNotExist:
                messages.error(request, "Brand not found.")
                return redirect('carbrand')
    except Exception as e:
        # messages.error(request, f"Error: {e}")
        return redirect('carbrand')



# Function for the Year model

def car_year(request):
    """This method is use to render the main page for car year and show the all saved year's list.

    Args:
        request

    Returns:
        Httprequest: This method is use for render the car year page.
    """
    page_obj = year_pagination(request)

    context = {
        'page_obj': page_obj,
        'curl':admincurl
    }

    return render(request, 'carmodel/car_year.html', context) 

def show_add_year(request):
    """This Method is allow to show the add year page with help of htmx request. 

    Args:
        request

    Returns:
        Httprequest: If success render the page for add years if fail render on caryear or main page.
    """
    page_obj = brand_pagination(request)

    context = {
        'curl':admincurl,
        'page_obj': page_obj
    }
    return render(request, 'carmodel/showaddyear.html',  context)

def add_year(request):
    """This Method is allow to insert the another year of car itno the database. 

    Args:
        request

    Returns:
        Httprequest: Add the record and if success redirect on the caryear page and if fail render on same page.
    """
    try:
        edit_year_obj = year_pagination(request)
        page_obj = brand_pagination(request)
        count = 1

        context = {
            'count':count,
            'curl':admincurl,
            'page_obj': page_obj,
            'edit_year_obj':edit_year_obj,
        }
        if request.method == 'POST':
            form = Addyearform(request.POST)    
            try:
                data = {
                    'car_id':request.POST.get('car_id'),
                    'year':request.POST.get('year'),
                }
                print('car_id',request.POST.get('car_id'))
                print('year',request.POST.get('year'))
                validate_car_year(data)
                if form.is_valid():
                    year = form.save(commit=False)
                    year_input = request.POST['year']
                    token = hashlib.sha256(year_input.encode()).hexdigest()
                    year.remember_token = token
                    form.save()
                    page_obj = year_pagination(request)

                    context = {
                        'curl':admincurl,
                        'page_obj': page_obj
                    }
                    messages.success(request, "One more car year has been added successfully!")
                    return render(request, 'carmodel/car_year.html', context)
                
                else:
                    messages.error(request, 'Invalid request, Try again')
                    return render (request, 'carmodel/car_year.html', context) 
            
            except fastjsonschema.exceptions.JsonSchemaValueException as e:
                messages.error(request,schemas.car_management_schemas.car_year_schema.
                get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
                return render(request, 'car_brand.html', {'form': Addbrandform()}, status=400)
            
            except json.JSONDecodeError:
                messages.error(request, f"{e}")
                return render(request, 'car_brand.html', {'form': Addbrandform()}, status=400)
                
            except Exception as e:
                messages.error(request, f"{e}")
                return render (request, 'carmodel/car_year.html', context)
        
    except Exception as e:
        # messages.error(request, f"{e}")
        return render (request, 'carmodel/car_year.html', context)

def edit_year(request, id):
    """
    Updates the details of a car year based on the provided form data. It then attempts to update the brand's details using the data 
    submitted through the HTTP request. If the update operation is successful, the user is redirected to the main car year listing page.

    Args::
    - request (HttpRequest): The incoming HTTP request containing the form data for updating the year.
    - year_id (int): The unique identifier of the car year to be updated.

    Returns:
    - HttpResponseRedirect: Redirects to the main car year listing page if the update is successful.
    - HttpResponse: Renders the update form template with the submitted data and validation errors if the update fails.

    """
    if request.method == 'GET':
        page_obj = brand_pagination(request)
        edit_year_obj = CarYear.objects.get(id=id)
        context = {
                'page_obj': page_obj,
                'edit_year_obj':edit_year_obj,
                'curl':admincurl,
            }
        return render(request, 'carmodel/year_edit.html', context)
    
    try:
        page_obj = year_pagination(request)
        context = {
                'page_obj': page_obj,   
                'curl':admincurl,   
            }
        if request.method == 'POST':
            year = CarYear.objects.get(id=id)
            old_brand = year.car_id
            old_year = year.year
            car_id = request.POST.get('car_id')

            if car_id:
                year.car_id = CarBrand.objects.get(id=int(car_id))
            else:
                year.car_id = old_brand
            
            year.year = request.POST.get('year', old_year)
            year.status = request.POST.get('status', 1)
            year.remember_token = year.remember_token
            year.save()
            messages.success(request, 'Brand is updated successfully!')
            return redirect('caryear')
        else:
            messages.error(request, 'Invalid inputs, try again')
            return render(request, 'carmodel/car_year.html', context)

    except Exception as e:
        messages.error(request, f"{e}")
    return render(request, 'carmodel/year_edit.html')
        
@csrf_exempt
def delete_year(request, id):
    """This method is allow to Delete year record with the confirmation popup

    Args:
        request (_type_): _description_.
        id (integer): Thi is year record id .

    Returns:
        Httprequest: if the year id is available the render it on the car_year page withh success 
        message and if not than show the error on same page.
    """
    try:
        Year = CarYear.objects.get(id=id)
        Year.delete()
        page_obj = year_pagination(request)
        
        context = {
            'page_obj': page_obj,
            'curl': request.build_absolute_uri(admincurl)
        }
        
        messages.success(request,f"{Year.car_id.brand} Year deleted successfully")
        return render(request, 'carmodel/car_year.html',context , status=200)
    
    except ObjectDoesNotExist:
        # Handle case where the object does not exist
        messages.error(f"Car year with id {id} does not exist.")
        return render(request, 'carmodel/car_year.html', context, status=404)
    
    except Exception as e:  
        messages.error(f"Error: {str(e)}")
        return render(request, 'carmodel/car_year.html', context, status=500)



# Function for the Car Models model

def car_model(request):
    """This method is use to render the main page for car model and show the all saved model's list.

    Args:
        request

    Returns:
        Httprequest: This method is use for render the car model page.
    """
    page_obj = model_pagination(request)

    context = {
        'curl':admincurl,
        'page_obj': page_obj
    }
    return render(request, 'carmodel/car_model.html', context)

def show_add_model(request):
    """This Method is allow to show the add model page with help of htmx request. 

    Args:
        request

    Returns:
        Httprequest: If success render the page for add model if fail render on carmodel or main page.
    """
    page_obj = brand_pagination(request)
    year_obj = year_pagination(request)

    context = {
        'curl':admincurl,
        'page_obj': page_obj,
        'year_obj': year_obj
    }
    return render(request, 'carmodel/showaddmodel.html',  context)

def add_model(request):
    """This Method is allow to insert the another model of car itno the database. 

    Args:
        request

    Returns:
        Httprequest: Add the record and if success redirect on the carmodel page and if fail render on same page.
    """
    try:
        page_obj = model_pagination(request)

        context = {
            'curl': admincurl,
            'page_obj': page_obj
        }
        if request.method == 'POST':
            form = Addmodelform(request.POST)
            count = 1

            context = {
                'curl': admincurl,
                'count': count
            }
            try:
                if form.is_valid():
                    model = form.save(commit=False)
                    
                    model_name = request.POST['model_name']
                    token = hashlib.sha256(model_name.encode()).hexdigest()
                    model.remember_token = token
                    model.save()  # Save the model instance
                    
                    page_obj = model_pagination(request)

                    context = {
                        'curl': admincurl,
                        'page_obj': page_obj
                    }
                    messages.success(request, "One more car model has been added successfully!")
                    return render(request, 'carmodel/car_model.html', context)
                
                else:
                    messages.error(request, 'Invalid request, Try again')
                    return render(request, 'carmodel/car_model.html', context) 
                
            except Exception as e:
                messages.error(request, f"{e}")
                return render(request, 'carmodel/car_model.html', context)
        
    except Exception as e:
        messages.error(request, f"{e}")
        return render(request, 'carmodel/car_model.html', context)
    
@csrf_exempt
def delete_model(request, id):
    """This method is allow to Delete model record with the confirmation popup

    Args:
        request (_type_): _description_.
        id (integer): Thi is model record id .

    Returns:
        Httprequest: if the model id is available the render it on the car_model page withh success 
        message and if not than show the error on same page.
    """
    try:
        model = CarModel.objects.get(id=id)
        model.delete()
        page_obj = model_pagination(request)
        
        context = {
            'page_obj': page_obj,
            'curl': request.build_absolute_uri(admincurl)
        }
        messages.success(request,f"{model.model_name} model deleted successfully")
        return render(request, 'carmodel/car_model.html',context , status=200)
    
    except ObjectDoesNotExist:
        # Handle case where the object does not exist
        messages.error(f"Car model with id {id} does not exist.")
        return render(request, 'carmodel/car_model.html', context, status=404)
    
    except Exception as e:  
        messages.error(f"Error: {str(e)}")
        return render(request, 'carmodel/car_model.html', context, status=500)
    
@csrf_exempt
def edit_model(request, id):
    """
    Updates the details of a car model based on the provided form data. It then attempts to update the model's details using the data 
    submitted through the HTTP request. If the update operation is successful, the user is redirected to the main car model listing page.

    Args::
    - request (HttpRequest): The incoming HTTP request containing the form data for updating the model.
    - year_id (int): The unique identifier of the car model to be updated.

    Returns:
    - HttpResponseRedirect: Redirects to the main car model listing page if the update is successful.
    - HttpResponse: Renders the update form template with the submitted data and validation errors if the update fails.

    """
    if request.method == 'GET':
        page_obj = brand_pagination(request)
        year_obj = year_pagination(request)
        edit_model_obj = CarModel.objects.get(id=id)
        context = {
                'curl':admincurl,
                'year_obj':year_obj,
                'page_obj': page_obj,
                'edit_model_obj':edit_model_obj,
            }
        return render(request, 'carmodel/model_edit.html', context)
    
    try:
        page_obj = model_pagination(request)
        context = {
                'page_obj': page_obj,   
                'curl':admincurl,   
            }
                        
        if request.method == 'POST':
            model = CarModel.objects.get(id=id)
            old_model = model.model_name
            car_id = request.POST.get('car_id')
            year_id = request.POST.get('year_id')
            old_year = CarYear.objects.get(id=int(model.year_id.id))
            old_brand = CarBrand.objects.get(id=int(model.car_id.id))

            if car_id:
                model.car_id = CarBrand.objects.get(id=int(car_id))
            else:
                model.car_id = old_brand
            
            if year_id:
                model.year_id = CarYear.objects.get(id=int(year_id))
            else:
                model.year_id = old_year
            
            model.status = request.POST.get('status', 1)
            model.model_name = request.POST.get('model_name', old_model)
            model.remember_token = model.remember_token
            model.save()

            messages.success(request, 'Model updated successfully!')
            return redirect('carmodel')
        
        else:
            messages.error(request, 'Invalid inputs, try again')
            return render(request, 'carmodel/car_model.html', context)

    except Exception as e:
        messages.error(request, f"{e}")
    return render(request, 'carmodel/model_edit.html')



# Function for the Car Car model
def car_trim(request):
    """This method is use to render the main page for car trim and show the all saved trim's list.

    Args:
        request

    Returns:
        Httprequest: This method is use for render the car trim page.
    """
    page_obj = trim_pagination(request)
    brand_obj = brand_pagination(request)
    year_obj = year_pagination(request)
    context ={
        'curl':admincurl,
        'page_obj':page_obj,
        'brand_obj':brand_obj,
        'year_obj':year_obj
    }
    return render(request, 'carmodel/car_trim.html', context)

def show_add_trim(request):
    """This Method is allow to show the add trim page with help of htmx request. 

    Args:
        request

    Returns:
        Httprequest: If success render the page for add trim if fail render on carmodel or main page.
    """
    page_obj = model_pagination(request)
    brand_obj = brand_pagination(request)
    year_obj = year_pagination(request)
    context ={
        'curl':admincurl,
        'page_obj':page_obj,
        'brand_obj':brand_obj,
        'year_obj':year_obj
    }
    
    return render(request, 'carmodel/showaddtrim.html',context)

def add_trim(request):
    """This Method is allow to insert the another trim of car itno the database. 

    Args:
        request

    Returns:
        Httprequest: Add the record and if success redirect on the cartrim page and if fail render on same page.
    """
    try:
        page_obj = model_pagination(request)
        brand_obj = brand_pagination(request)
        year_obj = year_pagination(request)
        context ={
            'curl':admincurl,
            'page_obj':page_obj,
            'brand_obj':brand_obj,
            'year_obj':year_obj
        }
        if request.method == 'POST':
            form = Addtrimform(request.POST)
            # page_obj = brand_pagination(request)
            count=1

            context = {
                'page_obj': page_obj,
                'curl':admincurl,
                'count':count
            }
            try:
                if form.is_valid():
                    trim = form.save(commit=False)
                    trim_name = request.POST['car_trim_name']
                    token = hashlib.sha256(trim_name.encode()).hexdigest()
                    trim.remember_token = token
                    form.save()
                    page_obj = trim_pagination(request)

                    context = {
                        'curl':admincurl,
                        'page_obj': page_obj
                    }
                    messages.success(request, "One more car trim has been added successfully!")
                    return render(request, 'carmodel/car_trim.html', context)
                
                else:
                    messages.error(request, 'Invalid request, Try again')
                    return render (request, 'carmodel/car_trim.html', context) 
                
            except Exception as e:
                messages.error(request, f"{e}")
                return render (request, 'carmodel/car_trim.html', context)
        
    except Exception as e:
        messages.error(request, f"{e}")
    return render (request, 'carmodel/car_trim.html',context)

@csrf_exempt
def delete_trim(request, id):
    """This method is allow to Delete trim record with the confirmation popup

    Args:
        request (_type_): _description_.
        id (integer): This is trim record id .

    Returns:
        Httprequest: if the trim id is available the render it on the car_trim page withh success 
        message and if not than show the error on same page.
    """
    try:
        trim = CarTrim.objects.get(id=id)
        trim.delete()
        page_obj = trim_pagination(request)
        
        context = {
            'page_obj': page_obj,
            'curl': request.build_absolute_uri(admincurl)
        }
        messages.success(request,f"{trim.car_trim_name} model deleted successfully")
        return render(request, 'carmodel/car_trim.html',context , status=200)
    
    except ObjectDoesNotExist:
        # Handle case where the object does not exist
        messages.error(f"Car model with id {id} does not exist.")
        return render(request, 'carmodel/car_trim.html', context, status=404)
    
    except Exception as e:  
        messages.error(f"Error: {str(e)}")
        return render(request, 'carmodel/car_trim.html', context, status=500)
        
@csrf_exempt
def edit_trim(request, id):
    """
    Updates the details of a car trim based on the provided form data. It then attempts to update the trim's details using the data 
    submitted through the HTTP request. If the update operation is successful, the user is redirected to the main car trim listing page.

    Args::
    - request (HttpRequest): The incoming HTTP request containing the form data for updating the trim.
    - year_id (int): The unique identifier of the car trim to be updated.

    Returns:
    - HttpResponseRedirect: Redirects to the main car trim listing page if the update is successful.
    - HttpResponse: Renders the update form template with the submitted data and validation errors if the update fails.

    """
    if request.method == 'GET':
        year_obj = year_pagination(request)
        page_obj = brand_pagination(request)
        model_obj = model_pagination(request)
        edit_trim_obj = CarTrim.objects.get(id=id)
        context = {
                'curl':admincurl,
                'year_obj':year_obj,
                'page_obj': page_obj,
                'model_obj':model_obj,
                'edit_trim_obj':edit_trim_obj,
            }
        return render(request, 'carmodel/trim_edit.html', context)
    
    try:
        page_obj = trim_pagination(request)
        context = {
                'page_obj': page_obj,   
                'curl':admincurl,   
            }
                        
        if request.method == 'POST':
            trim = CarTrim.objects.get(id=id)
            old_trim = trim.car_trim_name
            car_id = request.POST.get('car_id')
            year_id = request.POST.get('year_id')
            model_id = request.POST.get('model_id')
            old_year = CarYear.objects.get(id=int(trim.year_id.id))
            old_brand = CarBrand.objects.get(id=int(trim.car_id.id))
            old_model = CarModel.objects.get(id=int(trim.model_id.id))

            if car_id:
                trim.car_id = CarBrand.objects.get(id=int(car_id))
            else:
                trim.car_id = old_brand  
            
            if year_id:
                trim.year_id = CarYear.objects.get(id=int(year_id)) 
            else:
                trim.year_id = old_year

            if model_id:
                trim.model_id = CarModel.objects.get(id=int(model_id))
            else:
                trim.model_id = old_model
            
            trim.car_trim_name = request.POST.get('car_trim_name',old_trim)
            trim.status = request.POST.get('status',trim.status)
            trim.remember_token = trim.remember_token
            trim.save()

            messages.success(request, 'Trim is updated successfully!')
            return redirect('cartrim')
        else:
            messages.error(request, 'Invalid inputs, try again')
            return render(request, 'carmodel/car_trim.html', context)

    except Exception as e:
        messages.error(request, f"{e}")
    return render(request, 'carmodel/car_trim.html')