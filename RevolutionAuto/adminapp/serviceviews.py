import json
import schemas
import fastjsonschema
import schemas.service_schema

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist 
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from .models import ServiceType, ServiceCategory, Services, SubServices
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from .forms import AddServiceTypeForm, AddServiceCategoryForm, AddServicsForm, AddSubServiceForm
from adminapp.utils.utils import service_type_pagination,service_category_pagination, services_pagination, sub_services_pagination
from schemas.service_schema import validate_service_type_details, validate_service_category_details, validate_services_details, validate_sub_service_details

curl = settings.CURRENT_URL
admincurl = f"{curl}/admin/"

context = {
    'curl': admincurl,
}

# ---------------Service type views---------------

def service_type_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """This Method is used to show the form and add new service type itno the database. 

    Args:
        request: The incoming HTTP request containing form for add the service type.

    Returns:
        Httprequest: When get request show the form for add new service type and if post process a logic for Added the recored and if success 
        redirect on the same page and if fail render on same page with error message.
    """
    try:
        if request.method == 'GET':
            
            page_obj = service_type_pagination(request)

            context = {
                'curl': admincurl,
                'page_obj': page_obj
            }
            return render(request, 'service/service_type.html', context)
        
        elif request.method == 'POST':

            form = AddServiceTypeForm(request.POST)
            data = {
                'service_type_name': request.POST.get('service_type_name')
            }
            validate_service_type_details(data)

            if form.is_valid():
                form.save()

                page_obj = service_type_pagination(request)
                context = {
                    'curl': admincurl,
                    'page_obj':page_obj
                }
                messages.success(request, "Added Successfully!!")
                return render(request, 'service/service_type.html', context)
            
            else:
                messages.error(request, "In-valid input try again ")
                return render(request, 'service/service_type.html', context)   
        else:

            page_obj = service_type_pagination(request)
            context = {
                'curl': admincurl,
                'page_obj': page_obj
            }
            return render(request, 'service/service_type.html', context)
            
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.service_schema.service_type_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return render(request, 'service/service_type.html')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return render(request, 'service/service_type.html')            

    except Exception as e:
        messages.error(request, f"Unexpected error occur, Try again")
        return render(request, 'service/service_type.html')

@csrf_exempt
def service_type_action_handler(request: HttpRequest, id:int) -> HttpResponse | HttpResponseRedirect:
    """This method is allow to Delete service type record with the confirmation popup

    Args:
        request: The incoming HTTP request containing the data of a service type for delete.
        id (integer): This is service type record id 

    Returns:
        Httprequest: if the service type id is available than delet it and render it on the service type page with success 
        message and if not than show the error on same page.
    """
    try:
        if request.method == 'POST':
            servicecat = ServiceType.objects.get(id=id)
            old_service_type_name = servicecat.service_type_name
            old_service_status = servicecat.status
            data = {
                'service_type_name': request.POST.get('service_type_name')
            }
            validate_service_type_details(data)

            servicecat.service_type_name = request.POST.get('service_type_name', old_service_type_name)
            servicecat.status = request.POST.get('status', old_service_status)
            servicecat.save()

            messages.success(request, 'Updated successfully!')
            return redirect('service_type_data_handler')
        
        elif request.method == 'DELETE':
            
            servicetype = ServiceType.objects.get(id=id)
            servicetype.delete()
            page_obj = service_type_pagination(request)
            context = {
                'curl':admincurl,
                'page_obj':page_obj
            }
            messages.success(request, "Deleted successfully!!")
            return render(request, 'service/service_type.html', context)
    
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request, schemas.service_schema.service_type_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'Please enter valid data'))
        return redirect('service_type_data_handler')

    except json.JSONDecodeError as e:
        messages.error(request, f"{e}")
        return redirect('service_type_data_handler')            
    
    except ObjectDoesNotExist:
        messages.error(request, f"Service type does not exist.")
        return render(request, 'service/service_type.html')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin_dashboard.html')


# ---------------Service category views---------------

def service_category_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """This method is use to render the main page for service category and show the service category list

    Args:
        request: The incoming HTTP request containing the all service category data.

    Returns:
        Httprequest: This method is use for render the service category page.
    """
    try:

        if request.method == 'GET':
            page_obj = service_category_pagination(request)
            service_type = service_type_pagination(request)
            context = {
                'curl':admincurl,
                'page_obj':page_obj,
                'service_type':service_type
            }
            return render(request, 'service/service_category.html', context) 
        
        elif request.method == 'POST':
            form = AddServiceCategoryForm(request.POST)
            data = {
                'service_type' : request.POST.get("service_type"),
                'service_category_name' : request.POST.get("service_category_name"),
            }
            validate_service_category_details(data)

            if form.is_valid():
                form.save()
                page_obj = service_category_pagination(request)
                context = {
                    'curl':admincurl,
                    'page_obj':page_obj
                }
                messages.error(request, 'Added Successfully!!!')
                return redirect('service_category_data_handler')
        else:

            page_obj = service_category_pagination(request)
            service_type = service_type_pagination(request)
            context = {
                'curl':admincurl,
                'page_obj':page_obj,
                'service_type':service_type
            }
            return render(request, 'service/service_category.html', context)
            
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.service_schema.service_category_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect ( 'service_category_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect ( 'service_category_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin_dashboard.html')

@csrf_exempt
def service_category_action_handler(request: HttpRequest, id:int) -> HttpResponse | HttpResponseRedirect:
    """This method is allow to Delete service category record with the confirmation popup

    Args:
        request: The incoming HTTP request containing the data of a service category for delete.
        id (integer): This is service category record id 

    Returns:
        Httprequest: if the service category id is available than delete it and render it on the service category page with success 
        message and if not than show the error on same page.
    """
    try:
        if request.method == 'POST':

            service_type = request.POST.get('service_type')
            service_category_name = request.POST.get('service_category_name')
            data = {
                'service_type': service_type,
                'service_category_name': service_category_name
            }
            validate_service_category_details(data)

            # Get old Details
            servicecategory = ServiceCategory.objects.get(id=id)
            old_service_category_name = servicecategory.service_category_name
            old_status = servicecategory.status
            old_service_type = ServiceType.objects.get(id=int(servicecategory.service_type.id))

            # Update Details 
            servicecategory.status = request.POST.get('status', old_status)
            servicecategory.service_category_name = request.POST.get('service_category_name', old_service_category_name)
            servicecategory.service_type = ServiceType.objects.get(id=int(service_type)) if service_type else old_service_type

            servicecategory.save()

            page_obj = service_category_pagination(request)
            context = {
                'curl':admincurl,
                'page_obj':page_obj
            }
            messages.success(request, 'Updated successfully!')
            return redirect('service_category_data_handler')
        
        if request.method == 'DELETE':   

            servicecategory = ServiceCategory.objects.get(id=id)
            if servicecategory:

                servicecategory.delete()
                page_obj = service_category_pagination(request)
                context = {
                    'curl':admincurl,
                    'page_obj':page_obj
                }

                messages.success(request, f'Delete Successfully')
                return render(request, 'service/service_category.html', context) 
            
            else:
                messages.error(request, f"This service category is not found")
                return redirect('service_category_data_handler')
            
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.service_schema.service_category_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect ( 'service_category_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect ( 'service_category_data_handler')
        
    except ObjectDoesNotExist:
        messages.error(request, f"Service category does not exist.")
        return redirect('service_category_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin_dashboard.html')
 

# ---------------Services views---------------

@csrf_exempt
def service_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """This method is use to render the main page for service and show the service list

    Args:
        request: The incoming HTTP request containing the all service data.

    Returns:
        Httprequest: This method is use for render the service page.
    """
    try:
        if request.method == 'GET':
            page_obj = services_pagination(request)
            service_category = service_category_pagination(request)
            context = {
                'curl':admincurl,
                'page_obj':page_obj,
                'service_category':service_category
            }
            
            return render(request, 'service/services.html', context) 
        
        elif request.method == 'POST':

            form = AddServicsForm(request.POST)
            data = {
                'service_category': request.POST.get('service_category'),
                'service_title': request.POST.get('service_title'),
                'service_description': request.POST.get('service_description'),
            }
            validate_services_details(data)

            if form.is_valid():

                form.save()
                page_obj = services_pagination(request)
                context = {
                    'curl':admincurl,
                    'page_obj':page_obj
                }
                messages.success(request,"Added successfully!!!")
                return redirect('service_data_handler')
        else:
            messages.error(request,"invalid request, try again")
            return redirect('service_data_handler') 
            
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.service_schema.services_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect ( 'service_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect ( 'service_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin_dashboard.html')
    
@csrf_exempt
def service_action_handler(request: HttpRequest, id:int) -> HttpResponse:
    """
    Updates the details of a service based on the provided form data.
    
    Args:
    - request (HttpRequest): The incoming HTTP request containing the form data for updating the service.
    - id (int): The unique identifier of the service to be updated.
    
    Returns:
    - HttpResponseRedirect: Redirects to the main service listing page if the update is successful and if fails than
        renders the update form template with the submitted data and validation errors.
    """
    try:        
        if request.method == 'POST':
            service = Services.objects.get(id=id)

            service_title = request.POST.get('service_title')
            service_category = request.POST.get('service_category')
            service_description = request.POST.get('service_description')

            data = {
                'service_title':service_title,
                'service_category':service_category,
                'service_description':service_description,
            }
            validate_services_details(data)

            # Get existing or old data
            old_service_category = ServiceCategory.objects.get(id=int(service.service_category.id))
            old_service_title = service.service_title
            old_service_description = service.service_description

            # Update new or existing data
            service.status = request.POST.get('status', 1)
            service.service_title = request.POST.get('service_title', old_service_title)
            service.service_description = request.POST.get('service_description', old_service_description)
            service.service_category = ServiceCategory.objects.get(id=int(service_category)) if service_category else old_service_category

            messages.success(request, 'Update successfully!!')
            return redirect('service_data_handler')
        
        if request.method == 'DELETE':

            service = Services.objects.get(id=id)
            if service:
                service.delete()
                messages.success(request, 'Deleted successfully')
                return redirect('service_data_handler')
            
            else:
                messages.error(request, f'This service is not found')
                return redirect('service_data_handler')
    
    except ObjectDoesNotExist:
        messages.error(request ,f"Service category does not exist.")
        return redirect('service_data_handler')
        
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.service_schema.services_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect ( 'service_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect ( 'service_data_handler')

    except Exception as e:
        return redirect('service_data_handler')

# ---------------Sub-services views---------------

def sub_services_data_handler(request: HttpRequest):
    try:
        if request.method == 'GET':
            page_obj = sub_services_pagination(request)
            services = services_pagination(request)
            context = {
                'curl':admincurl,
                'page_obj':page_obj,
                'services':services
            }
            return render(request, 'service/sub_service.html',context)
        
        elif request.method == 'POST':
            form = AddSubServiceForm(request.POST)

            if form.is_valid():
                service = request.POST.get('service')
                order = request.POST.get('order')
                selection_type = request.POST.get('selection_type')
                optional = request.POST.get('optional')
                
                try:
                    data_validate = SubServices.objects.get(service=service, order=order, selection_type=selection_type, optional=optional)

                except SubServices.DoesNotExist:
                        form.save()
                        messages.success(request, 'Added Successful')
                        return redirect('sub_services_data_handler')
                
                except SubServices.MultipleObjectsReturned:
                        messages.error(request, 'Same record already available, try again')
                        return redirect('sub_services_data_handler')
            else:
                messages.error(request, 'error')
                return redirect('sub_services_data_handler')

        else:
            messages.error(request, 'Invalid request, try again')
            return redirect('sub_services_data_handler')
            
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin_dashboard.html')
    
    except Exception as e:
        messages.error(request, f"{e}")
        return render(request, 'service/sub_service.html')
    

def sub_services_action_handler(request: HttpRequest, id: int) -> HttpResponse:

    if request.method == 'POST':
            print('working')
            service = Services.objects.get(id=id)

            service_title = request.POST.get('service_title')
            service_category = request.POST.get('service_category')
            service_description = request.POST.get('service_description')

            data = {
                'service_title':service_title,
                'service_category':service_category,
                'service_description':service_description,
            }
            validate_services_details(data)

            # Get existing or old data
            old_service_category = ServiceCategory.objects.get(id=int(service.service_category.id))
            old_service_title = service.service_title
            old_service_description = service.service_description

            # Update new or existing data
            service.status = request.POST.get('status', 1)
            service.service_title = request.POST.get('service_title', old_service_title)
            service.service_description = request.POST.get('service_description', old_service_description)
            service.service_category = ServiceCategory.objects.get(id=int(service_category)) if service_category else old_service_category

    messages.success(request, 'Update successfully!!')
    return redirect('service_data_handler')