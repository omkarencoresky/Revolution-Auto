import os
import json
import hashlib
import schemas
import fastjsonschema
from django.conf import settings
from django.contrib import messages
import schemas.car_management_schemas
from schemas import car_management_schemas
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import never_cache
from .models import CarBrand, CarYear, CarModel, CarTrim
from django.contrib.auth.decorators import login_required
from .forms import AddBrandForm, AddYearForm, AddModelForm, AddTrimForm
from adminapp.utils.utils import brand_pagination, year_pagination, model_pagination, trim_pagination

curl = settings.CURRENT_URL
admincurl = f"{curl}/admin/"
media_path = f'{settings.MEDIA_URL}'   


# Function for the brand model
@never_cache
@login_required
def car_brand_data_handler(request: HttpRequest) -> HttpResponse:
    """This method is use to render the main page for car brand and show the brand's list

    Args:
        request: The incoming HTTP request containing the all car data.

    Returns:
        Httprequest: This method is use for render the car brand page.
    """
    try:    
        if request.method == 'GET':

            page_obj = brand_pagination(request)

            context = {
                'page_obj': page_obj,
                'curl':admincurl,
            }
            return render(request, 'carmodel/car_brand.html', context)
        
        elif request.method == 'POST':

            form = AddBrandForm(request.POST, request.FILES)
            page_obj = brand_pagination(request)

            context = {
                'page_obj': page_obj,
                'curl':admincurl,
            }

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

                context = {
                    'curl':admincurl,
                    'page_obj': page_obj,
                }
                messages.success(request, "Added successfully!")
                return render(request, 'carmodel/car_brand.html', context)
            
        else:
            messages.error(request, 'Invalid request, Try again')
            return render(request, 'carmodel/car_brand.html', context) 
            
            
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.car_management_schemas.car_brand_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect ( 'car_brand_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect ( 'car_brand_data_handler')
        
    except Exception as e:
        messages.error(request,f"{e}")
        return render(request, 'admin_dashboard.html')


@never_cache
@login_required
@csrf_exempt
def car_brand_action_handler(request: HttpRequest, id: int) -> HttpResponse:
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

        if request.method == 'POST':

            brand = CarBrand.objects.get(id=id)
            context = {
            'page_obj': brand_pagination(request),
            'curl': admincurl,
            'brand': brand,
            }
            
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
            return redirect('car_brand_data_handler')
        
        elif request.method == 'DELETE':
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
            
            messages.success(request,f"Deleted successfully")
            return render(request, 'carmodel/car_brand.html',context , status=200)
        else:
            messages.error(request, 'Invalid request, Try again')
            return render(request, 'carmodel/car_brand.html') 
            
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
            messages.error(request,schemas.car_management_schemas.car_brand_schema.
            get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
            return redirect('car_brand_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('car_brand_data_handler')
    
    except ObjectDoesNotExist:
        messages.error(request, "Brand not found.")
        return redirect('car_brand_data_handler')
            
    except Exception as e:
        # messages.error(request, f"Error: {e}")
        return redirect('car_brand_data_handler')



# Function for the Year model
@never_cache
@login_required
def car_year_data_handler(request: HttpRequest) -> HttpResponse:
    """This method is use to render the main page for car year and show the all saved year's list.

    Args:
        request: The incoming HTTP request containing all the data of the year list.

    Returns:
        Httprequest: This method is use for render the car year page.
    """
    try:
        if request.method == 'GET':

            page_obj = year_pagination(request)
            brands = brand_pagination(request)
            context = {
                'curl':admincurl,
                'page_obj': page_obj,
                'brands':brands
            }

            return render(request, 'carmodel/car_year.html', context) 
        
        elif request.method == 'POST':
            form = AddYearForm(request.POST)    
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
                return redirect('car_year_data_handler')
            
        else:
            messages.error(request, 'Invalid request, Try again')
            return redirect('car_year_data_handler')
        
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.car_management_schemas.car_year_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect('car_year_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('car_year_data_handler')
    
    except Exception as e:
        messages.error(request, f"{e}")
        return redirect('car_year_data_handler')


@never_cache
@login_required
@csrf_exempt
def car_year_action_handler(request: HttpRequest, id: int) -> HttpResponse:
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
    
    try:
            
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
            return redirect('car_year_data_handler')
        
        elif request.method == 'DELETE':

            Year = CarYear.objects.get(id=id)
            Year.delete()
            page_obj = year_pagination(request)
            
            context = {
                'page_obj': page_obj,
                'curl': request.build_absolute_uri(admincurl)
            }
            
            messages.success(request,f"Deleted successfully")
            return render(request, 'carmodel/car_year.html',context , status=200)
        
        
        else:
            messages.error(request, 'Invalid inputs, try again')
            return redirect('car_year_data_handler')

    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.car_management_schemas.car_year_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect('car_year_data_handler')

    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('car_year_data_handler')
    
    except ObjectDoesNotExist:
        messages.error(f"Car year with id {id} does not exist.")
        return render(request, 'carmodel/car_year.html', context, status=404)

    except Exception as e:
        messages.error(request, f"{e}")
        return redirect('car_year_data_handler')
 

# Function for the Car Models model
@never_cache
@login_required
@csrf_exempt
def car_model_data_handler(request: HttpRequest) -> HttpResponse:
    """This method is use to render the main page for car model and show the all saved model's list.

    Args:
        request: The incoming HTTP request containing all the data of the model list.

    Returns:
        Httprequest: This method is use for render the car model page.
    """
    try:
        if request.method == 'GET':

            page_obj = model_pagination(request)
            brands = brand_pagination(request)
            years = year_pagination(request)

            context = {
                'curl':admincurl,
                'page_obj': page_obj,
                'brands':brands,
                'years':years
            }
            return render(request, 'carmodel/car_model.html', context)
        
        elif request.method == 'POST':

            form = AddModelForm(request.POST)
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
                return redirect('car_model_data_handler')
            
        else:
            messages.error(request, 'Invalid request, Try again')
            return redirect('car_model_data_handler') 
                    
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.car_management_schemas.car_model_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect('car_model_data_handler')

    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('car_model_data_handler')
    
    except Exception as e:
        messages.error(request,f"{e}")
        return render(request, 'admin_dashboard.html')


@never_cache
@login_required    
@csrf_exempt
def car_model_action_handler(request: HttpRequest, id: int) -> HttpResponse:
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
    try:
        if request.method == 'POST':
            car_id = request.POST.get('car_id')
            year_id = request.POST.get('year_id')

            data={
                'car_id':car_id,
                'year_id':year_id,
                'model_name':request.POST.get('model_name'),
            }
            car_management_schemas.validate_car_model_details(data)
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
            return redirect('car_model_data_handler')
        
        elif request.method == 'DELETE':

            model = CarModel.objects.get(id=id)
            model.delete()
            page_obj = model_pagination(request)
            brands = brand_pagination(request)
            years = year_pagination(request)

            context = {
                'curl':admincurl,
                'page_obj': page_obj,
                'brands':brands,
                'years':years
            }
            messages.success(request, f"Deleted successfully")
            return render(request, 'carmodel/car_model.html', context)
     
        else:
            messages.error(request, 'Invalid inputs, try again')
            return redirect('car_model_data_handler')
        
    except ObjectDoesNotExist:
        messages.error(f"Car model with id {id} does not exist.")
        return redirect('car_model_data_handler')
        
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.car_management_schemas.car_model_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect('car_model_data_handler')

    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('car_model_data_handler')

    except Exception as e:
        messages.error(request, f"{e}")
        return redirect('car_model_data_handler')



# Function for the Car trim
@never_cache
@login_required
def car_trim_data_handler(request: HttpRequest) -> HttpResponse:
    """This method is use to render the main page for car trim and show the all saved trim's list.

    Args:
        request: The incoming HTTP request containing all the data of the trims.

    Returns:
        Httprequest: This method is use for render the car trim page.
    """
    try:
        if request.method == 'GET':

            page_obj = trim_pagination(request)
            brands = brand_pagination(request)
            years = year_pagination(request)
            models = model_pagination(request)
            context ={
                'curl':admincurl,
                'page_obj':page_obj,
                'brands':brands,
                'years':years,
                'models':models
            }
            return render(request, 'carmodel/car_trim.html', context)

        elif request.method == 'POST':

            form = AddTrimForm(request.POST)
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
                messages.success(request, "Added successfully!")
                return redirect('car_trim_data_handler')
            
            else:
                messages.error(request, 'Invalid request, Try again')
                return redirect('car_trim_data_handler') 
        else:
                messages.error(request, 'Invalid request, Try again')
                return redirect('car_trim_data_handler') 
                
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.car_management_schemas.car_trim_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect('car_trim_data_handler')

    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('car_trim_data_handler')
    
    except Exception as e:
        messages.error(request,f"{e}")
        return render(request, 'admin_dashboard.html')



@never_cache
@login_required
@csrf_exempt
def car_trim_action_handler(request: HttpRequest, id: int) -> HttpResponse:
    """This method is allow to Delete trim record with the confirmation popup

    Args:
        request (_type_): _description_.
        id (integer): This is trim record id .

    Returns:
        Httprequest: if the trim id is available the render it on the car_trim page withh success 
        message and if not than show the error on same page.
    """
    try:
        if request.method == 'POST':
            car_id = request.POST.get('car_id')
            year_id = request.POST.get('year_id')
            model_id = request.POST.get('model_id')
            
            data = {
                'car_id':car_id,
                'year_id':year_id,
                'model_id':model_id,
                'car_trim_name':request.POST.get('car_trim_name')    
                }
            car_management_schemas.validate_car_trim_details(data)
                        
            trim = CarTrim.objects.get(id=id)
            old_trim = trim.car_trim_name
            old_year = CarYear.objects.get(id=int(trim.year_id.id))
            old_brand = CarBrand.objects.get(id=int(trim.car_id.id))
            old_model = CarModel.objects.get(id=int(trim.model_id.id))

            # Check new deails select than update 
            trim.car_id = CarBrand.objects.get(id=int(car_id)) if car_id else old_brand
            trim.year_id = CarYear.objects.get(id=int(year_id)) if year_id else old_year
            trim.model_id = CarModel.objects.get(id=int(model_id)) if model_id else old_model
            trim.car_trim_name = request.POST.get('car_trim_name',old_trim)
            trim.status = request.POST.get('status',trim.status)
            trim.remember_token = trim.remember_token
            
            # if year_id:
            #     trim.year_id = CarYear.objects.get(id=int(year_id)) 
            # else:
            #     trim.year_id = old_year

            trim.save()

            messages.success(request, 'Updated successfully!')
            return redirect('car_trim_data_handler')
        
        elif request.method == 'DELETE': 
            trim = CarTrim.objects.get(id=id)
            trim.delete()
            
            page_obj = trim_pagination(request)
            
            context = {
                'page_obj': page_obj,
                'curl': request.build_absolute_uri(admincurl)
            }
            messages.success(request,f"Deleted successfully")
            return render(request, 'carmodel/car_trim.html',context , status=200)
        
        else:
            messages.error(request, 'Invalid inputs, try again')
            return redirect('car_trim_data_handler')

    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.car_management_schemas.car_trim_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect('car_trim_data_handler')

    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('car_trim_data_handler')
    
    except ObjectDoesNotExist:
        messages.error(f"Car model with id {id} does not exist.")
        return render(request, 'carmodel/car_trim.html', context, status=404)
    
    except Exception as e:  
        messages.error(f"Error: {str(e)}")
        return render(request, 'carmodel/car_trim.html', context, status=500)
