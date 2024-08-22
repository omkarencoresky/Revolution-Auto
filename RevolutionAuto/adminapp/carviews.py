import os
import json
import hashlib
import schemas
import fastjsonschema
import schemas.car_management_schemas

from django.conf import settings
from django.contrib import messages
from schemas import car_management_schemas
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import CarBrand, CarYear, CarModel, CarTrim
from .forms import AddBrandForm, AddYearForm, AddModelForm, AddTrimForm
from adminapp.utils.utils import brand_pagination, year_pagination, model_pagination, trim_pagination

curl = settings.CURRENT_URL
admincurl = f"{curl}/adminapp/"
media_path = f'{settings.MEDIA_URL}'   


# Function for the brand model

def car_brand(request):
    """This method is use to render the main page for car brand and show the brand's list

    Args:
        request

    Returns:
        Httprequest: This method is use for render the car brand page.
    """
    try:
        page_obj = brand_pagination(request)

        context = {
            'page_obj': page_obj,
            'curl':admincurl
        }

        return render(request, 'carmodel/car_brand.html', context)
    except Exception as e:
        messages.error(request,f"{e}")
        return render(request, 'admin_dashboard.html')

def add_brand(request):
    """This Method is allow to insert the another one brand of car itno the database. 

    Args:
        request

    Returns:
        Httprequest: Added the recored and if success redirect on the same page and if fail render on same page
    """
    try:
        if request.method == 'POST':
            form = AddBrandForm(request.POST, request.FILES)
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
                    'image_format':image_format,
                    'brand':request.POST.get('brand'),
                    'description':request.POST.get('description'),
                }
                car_management_schemas.validate_car_brand_details(data)
                
                if form.is_valid():

                    brand = form.save(commit=False)
                    brand_name = request.POST['brand']
                    brand.image_url = f"{media_path}{image_name}"   
                    media_directory = os.path.join(settings.BASE_DIR, 'media')
                    file_path = os.path.join(media_directory, image_name)
                    token = hashlib.sha256(brand_name.encode()).hexdigest()
                    brand.remember_token = token

                    if not os.path.exists(media_directory):
                        os.makedirs(media_directory)

                    with open(file_path, "wb") as fp:
                        for chunk in uploaded_file.chunks():
                            fp.write(chunk)
                    form.save()

                    page_obj = brand_pagination(request)
                    count=1

                    context = {
                        'count':count,
                        'curl':admincurl,
                        'page_obj': page_obj,
                    }
                    messages.success(request, "Added successfully!")
                    return render(request, 'carmodel/car_brand.html', context)
                
                else:
                    messages.error(request, 'Invalid inputs in this form, Try again')
                    return redirect ( 'carbrand') 
                
            except fastjsonschema.exceptions.JsonSchemaValueException as e:
                messages.error(request,schemas.car_management_schemas.car_brand_schema.
                get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
                return redirect ( 'carbrand')
            
            except json.JSONDecodeError:
                messages.error(request, f"{e}")
                return redirect ( 'carbrand')
            
            except Exception as e:
                messages.error(request, f"Invalid input of this field {e}" )
                return redirect ( 'carbrand')
        
    except Exception as e:
        return render (request, 'carmodel/car_brand.html', context)

def show_add_brand(request):
    """This Method is allow to show the add brand page withe help of htmx request. 

    Args:
        request

    Returns:
        Httprequest: If success render the page page for add brands if fail render car brand or main.
    """
    try:
        context = {
            'curl':admincurl,
        }
        return render(request, 'carmodel/show_add_brand.html', context)
    except Exception as e:
        messages.error(request,f"{e}")
        return render(request, 'admin_dashboard.html')

@csrf_exempt
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
        page_obj = brand_pagination(request)
            
        context = {
            'page_obj': page_obj,
            'curl': request.build_absolute_uri(admincurl)
        }
        brand = CarBrand.objects.get(id=id)
        brand.delete()

        page_obj = brand_pagination(request)
        context = {
            'page_obj': page_obj,
            'curl': request.build_absolute_uri(admincurl)
        }
        
        messages.success(request,f"{brand.brand} Deleted successfully")
        return render(request, 'carmodel/car_brand.html',context , status=200)
    
    except ObjectDoesNotExist:
        messages.error(request, f"CarBrand with id {id} does not exist.")
        return render(request, 'carmodel/car_brand.html', context, status=404)
    
    except Exception as e:  
        messages.error(f"Error: {str(e)}")
        return render(request, 'carmodel/car_brand.html', context, status=500) 

@csrf_exempt 
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
                    'brand': brand,
                    'curl': admincurl,
                    'page_obj': brand_pagination(request),
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
                    'image_format':image_format,
                    'brand':request.POST.get('brand'),
                    'description':request.POST.get('description'),
                }
                car_management_schemas.validate_car_brand_details(data)
                brand = CarBrand.objects.get(id=id)

                brand.brand = request.POST.get('brand', brand.brand)
                brand.status = request.POST.get('status', brand.status)
                brand.description = request.POST.get('description', brand.description)

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
                messages.success(request, 'Updated successfully!')
                return redirect('carbrand')
            except fastjsonschema.exceptions.JsonSchemaValueException as e:
                    messages.error(request,schemas.car_management_schemas.car_brand_schema.
                    get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
                    return redirect('carbrand')
            
            except json.JSONDecodeError:
                messages.error(request, f"{e}")
                return redirect('carbrand')
            
            except ObjectDoesNotExist:
                messages.error(request, "Brand not found.")
                return redirect('carbrand')
            
    except Exception as e:
        # messages.error(request, f"Error: {e}")
        return redirect('carbrand')




def car_year(request):
    """This method is use to render the main page for car year and show the all saved year's list.

    Args:
        request

    Returns:
        Httprequest: This method is use for render the car year page.
    """
    try:
        page_obj = year_pagination(request)

        context = {
            'curl':admincurl,
            'page_obj': page_obj,
        }

        return render(request, 'carmodel/car_year.html', context) 
    except Exception as e:
        messages.error(request,f"{e}")
        return render(request, 'admin_dashboard.html')

def show_add_year(request):
    """This Method is allow to show the add year page with help of htmx request. 

    Args:
        request

    Returns:
        Httprequest: If success render the page for add years if fail render on caryear or main page.
    """
    try:
        page_obj = brand_pagination(request)

        context = {
            'curl':admincurl,
            'page_obj': page_obj
        }
        return render(request, 'carmodel/show_add_year.html',  context)
    except Exception as e:
        messages.error(request,f"{e}")
        return render(request, 'admin_dashboard.html')

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

        context = {
            'curl':admincurl,
            'page_obj': page_obj,
            'edit_year_obj':edit_year_obj,
        }
        if request.method == 'POST':

            form = AddYearForm(request.POST)    
            try:
                data = {
                    'car_id':request.POST.get('car_id'),
                    'year':request.POST.get('year'),
                }
                car_management_schemas.validate_car_year_details(data)

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
                    messages.success(request, "Added successfully!")
                    return render(request, 'carmodel/car_year.html', context)
                
                else:
                    messages.error(request, 'Invalid request, Try again')
                    return redirect('caryear')
            
            except fastjsonschema.exceptions.JsonSchemaValueException as e:
                messages.error(request,schemas.car_management_schemas.car_year_schema.
                get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
                return redirect('caryear')
            
            except json.JSONDecodeError:
                messages.error(request, f"{e}")
                return redirect('caryear')
                
            except Exception as e:
                messages.error(request, f"{e}")
                return redirect('caryear')
        
    except Exception as e:
        # messages.error(request, f"{e}")
        return redirect('caryear')

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

            car_id = request.POST.get('car_id')
            data = {
                    'car_id':car_id,
                    'year':request.POST.get('year'),
                }
            car_management_schemas.validate_car_year_details(data)

            year = CarYear.objects.get(id=id)
            old_brand = year.car_id
            old_year = year.year

            if car_id:
                year.car_id = CarBrand.objects.get(id=int(car_id))
            else:
                year.car_id = old_brand
            
            year.remember_token = year.remember_token
            year.status = request.POST.get('status', 1)
            year.year = request.POST.get('year', old_year)
            year.save()

            messages.success(request, 'Updated successfully!')
            return redirect('caryear')
        
        else:
            messages.error(request, 'Invalid inputs, try again')
            return redirect('caryear')

    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.car_management_schemas.car_year_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect('caryear')

    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('caryear')

    except Exception as e:
        messages.error(request, f"{e}")
        return redirect('caryear')
        
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
        
        messages.success(request,f"{Year.car_id.brand} Deleted successfully")
        return render(request, 'carmodel/car_year.html',context , status=200)
    
    except ObjectDoesNotExist:
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
    try:
        page_obj = model_pagination(request)

        context = {
            'curl':admincurl,
            'page_obj': page_obj
        }
        return render(request, 'carmodel/car_model.html', context)
    except Exception as e:
        messages.error(request,f"{e}")
        return render(request, 'admin_dashboard.html')

def show_add_model(request):
    """This Method is allow to show the add model page with help of htmx request. 

    Args:
        request

    Returns:
        Httprequest: If success render the page for add model if fail render on carmodel or main page.
    """
    try:
        page_obj = brand_pagination(request)
        year_obj = year_pagination(request)

        context = {
            'curl':admincurl,
            'page_obj': page_obj,
            'year_obj': year_obj
        }
        return render(request, 'carmodel/show_add_model.html',  context)
    except Exception as e:
        messages.error(request,f"{e}")
        return render(request, 'admin_dashboard.html')

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
            form = AddModelForm(request.POST)
            context = {
                'curl': admincurl,
            }

            try:
                data={
                    'car_id':request.POST.get('car_id'),
                    'year_id':request.POST.get('year_id'),
                    'model_name':request.POST.get('model_name'),
                }
                car_management_schemas.validate_car_model_details(data)

                if form.is_valid():

                    model = form.save(commit=False)
                    model_name = request.POST['model_name']
                    token = hashlib.sha256(model_name.encode()).hexdigest()
                    model.remember_token = token
                    model.save()
                    
                    page_obj = model_pagination(request)
                    context = {
                        'curl': admincurl,
                        'page_obj': page_obj
                    }
                    
                    messages.success(request, "Added successfully!")
                    return render(request, 'carmodel/car_model.html', context)
                
                else:
                    messages.error(request, 'Invalid request, Try again')
                    return render(request, 'carmodel/car_model.html', context) 
                    
            except fastjsonschema.exceptions.JsonSchemaValueException as e:
                messages.error(request,schemas.car_management_schemas.car_model_schema.
                get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
                return redirect('carmodel')

            except json.JSONDecodeError:
                messages.error(request, f"{e}")
                return redirect('carmodel')
                
            except Exception as e:
                messages.error(request, f"{e}")
                return redirect('carmodel')
        
    except Exception as e:
        messages.error(request, f"{e}")
        return redirect('carmodel')
    
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
        messages.success(request,f"{model.model_name} Deleted successfully")
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
        
        car_id = request.POST.get('car_id')
        year_id = request.POST.get('year_id')

        data={
            'car_id':car_id,
            'year_id':year_id,
            'model_name':request.POST.get('model_name'),
        }
        car_management_schemas.validate_car_model_details(data)
                        
        if request.method == 'POST':
            model = CarModel.objects.get(id=id)
            old_model = model.model_name
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
            model.remember_token = model.remember_token
            model.model_name = request.POST.get('model_name', old_model)
            model.save()

            messages.success(request, 'Updated successfully!')
            return redirect('carmodel')
        
        else:
            messages.error(request, 'Invalid inputs, try again')
            return redirect('carmodel')
        
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.car_management_schemas.car_model_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect('carmodel')

    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('carmodel')

    except Exception as e:
        messages.error(request, f"{e}")
        return redirect('carmodel')



# Function for the Car Car model
def car_trim(request):
    """This method is use to render the main page for car trim and show the all saved trim's list.

    Args:
        request

    Returns:
        Httprequest: This method is use for render the car trim page.
    """
    try:
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
    except Exception as e:
        messages.error(request,f"{e}")
        return render(request, 'admin_dashboard.html')

def show_add_trim(request):
    """This Method is allow to show the add trim page with help of htmx request. 

    Args:
        request

    Returns:
        Httprequest: If success render the page for add trim if fail render on carmodel or main page.
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
        
        return render(request, 'carmodel/show_add_trim.html',context)
    except Exception as e:
        messages.error(request,f"{e}")
        return render(request, 'admin_dashboard.html')

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
            form = AddTrimForm(request.POST)

            context = {
                'page_obj': page_obj,
                'curl':admincurl,
            }
            try:
                trim_name = request.POST.get('car_trim_name')
                data = {
                    'car_id':request.POST.get('car_id'),
                    'year_id':request.POST.get('year_id'),
                    'model_id':request.POST.get('model_id'),
                    'car_trim_name':trim_name   
                    }
                car_management_schemas.validate_car_trim_details(data)
                if form.is_valid():
                    trim = form.save(commit=False)
                    token = hashlib.sha256(trim_name.encode()).hexdigest()
                    trim.remember_token = token
                    form.save()
                    page_obj = trim_pagination(request)

                    context = {
                        'curl':admincurl,
                        'page_obj': page_obj
                    }
                    messages.success(request, "Added successfully!")
                    return render(request, 'carmodel/car_trim.html', context)
                
                else:
                    messages.error(request, 'Invalid request, Try again')
                    return render (request, 'carmodel/car_trim.html', context) 
                
            except fastjsonschema.exceptions.JsonSchemaValueException as e:
                messages.error(request,schemas.car_management_schemas.car_trim_schema.
                get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
                return redirect('cartrim')

            except json.JSONDecodeError:
                messages.error(request, f"{e}")
                return redirect('cartrim')
                
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
        messages.success(request,f"{trim.car_trim_name} Deleted successfully")
        return render(request, 'carmodel/car_trim.html',context , status=200)
    
    except ObjectDoesNotExist:
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

        car_id = request.POST.get('car_id')
        year_id = request.POST.get('year_id')
        model_id = request.POST.get('model_id')
        page_obj = trim_pagination(request)
        
        context = {
                'page_obj': page_obj,   
                'curl':admincurl,   
            }
        
        data = {
            'car_id':car_id,
            'year_id':year_id,
            'model_id':model_id,
            'car_trim_name':request.POST.get('car_trim_name')    
            }
        car_management_schemas.validate_car_trim_details(data)
                        
        if request.method == 'POST':

            trim = CarTrim.objects.get(id=id)
            old_trim = trim.car_trim_name
            old_year = CarYear.objects.get(id=int(trim.year_id.id))
            old_brand = CarBrand.objects.get(id=int(trim.car_id.id))
            old_model = CarModel.objects.get(id=int(trim.model_id.id))

            trim.car_id = CarBrand.objects.get(id=int(car_id)) if car_id else old_brand
            trim.year_id = CarYear.objects.get(id=int(year_id)) if year_id else old_year
            trim.model_id = CarModel.objects.get(id=int(model_id)) if model_id else old_model
            
            # if year_id:
            #     trim.year_id = CarYear.objects.get(id=int(year_id)) 
            # else:
            #     trim.year_id = old_year

            trim.car_trim_name = request.POST.get('car_trim_name',old_trim)
            trim.status = request.POST.get('status',trim.status)
            trim.remember_token = trim.remember_token
            trim.save()

            messages.success(request, 'Updated successfully!')
            return redirect('cartrim')
        
        else:
            messages.error(request, 'Invalid inputs, try again')
            return redirect('cartrim')
        
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.car_management_schemas.car_trim_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect('cartrim')

    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('cartrim')

    except Exception as e:
        messages.error(request, f"{e}")
        return redirect('cartrim')