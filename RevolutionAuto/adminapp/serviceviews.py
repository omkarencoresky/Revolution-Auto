import os
import json
import schemas
import fastjsonschema
import schemas.service_schema

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist 
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from .models import ServiceType, ServiceCategory, Services, SubService, SubServiceOption, Inspection
from .forms import AddServiceTypeForm, AddServiceCategoryForm, AddServicsForm, AddSubServiceForm, AddSubServiceOptionForm
from adminapp.utils.utils import service_type_pagination,service_category_pagination, services_pagination, sub_services_pagination, inspection_pagination, sub_service_option_pagination
from schemas.service_schema import validate_service_type_details, validate_service_category_details, validate_services_details, validate_sub_service_details,validate_sub_service_option_details

curl = settings.CURRENT_URL
admincurl = f"{curl}/admin/"
media_path = f'{settings.MEDIA_URL}' 


# ---------------Service type views---------------

def service_type_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles displaying service_type list when the request type is GET and adding a new service_type when the request type is POST.

        Args:
            request: The incoming HTTP request. If GET, it shows the service_type list. If POST, it processes the logic for adding a new service_type.

        Returns:
            HttpResponse: For GET requests, it returns a response with the service_type list. For POST requests, if the user input is valid, it adds the 
            service_type and redirects to the main page. If the input is invalid, it renders the form with an error message and redirects to the main page.
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
                messages.success(request, "Added Successfully!")
                return render(request, 'service/service_type.html', context)
            
            else:
                messages.error(request, "In-valid input's try again ")
                return redirect('service_type_data_handler')   
        else:
            page_obj = service_type_pagination(request)
            context = {
                'curl':admincurl,
                'page_obj':page_obj
            }
            return render(request, 'service/service_type.html', context)
    
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.service_schema.service_type_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', "please enter the valid data"))
        return redirect('service_type_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect('service_type_data_handler')

    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin_dashboard.html')

    except Exception as e:
        messages.error(request, f"Unexpected error occur, Try again")
        return redirect('service_type_data_handler')

@csrf_exempt
def service_type_action_handler(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles updating service_type item when the request type is POST with an ID, and deleting service_type item when the request type is DELETE with an ID.

        Args:
            request: The incoming HTTP request. For POST requests, it updates the service_type specified by the ID in the request. For DELETE requests, it deletes the item specified by the ID.

        Returns:
            HttpResponse: For POST requests, if the update is successful, it redirects to the main page. If the update fails, it shows an error message and redirects to the main page. 
            For DELETE requests, if the deletion is successful, it redirects to the main page. If the deletion fails, it shows an error message and redirects to the main page.
    """
    try:
        if request.method == 'POST':
            servicecat = ServiceType.objects.get(id=id)

            data = {
                'service_type_name': request.POST.get('service_type_name')
                }
            validate_service_type_details(data)

            old_service_status = servicecat.status
            old_service_type_name = servicecat.service_type_name
            servicecat.status = request.POST.get('status', old_service_status)
            servicecat.service_type_name = request.POST.get('service_type_name', old_service_type_name)
            servicecat.save()

            messages.success(request, "Updated successfully!")
            return redirect('service_type_data_handler')
        
        elif request.method == 'DELETE':
            servicetype = ServiceType.objects.get(id=id)

            if servicetype:
                servicetype.delete()

                page_obj = service_type_pagination(request)
                context = {
                    'curl': admincurl,
                    'page_obj': page_obj
                }

                messages.success(request, "Deleted successfully!!")
                return render(request, 'service/service_type.html', context)
            
        else:
            messages.error(request, f"Unexpected error occur, Try again")
            return redirect('service_type_data_handler')            
    
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request, schemas.service_schema.service_type_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', "Please enter valid data"))
        return redirect('service_type_data_handler')

    except json.JSONDecodeError as e:
        messages.error(request, f"{e}")
        return redirect('service_type_data_handler')            
    
    except ObjectDoesNotExist:
        messages.error(request, f"Service type does not exist.")
        return redirect('service_type_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin_dashboard.html')
    
    except Exception as e:
        messages.error(request, f"Unexpected error occur, Try again")
        return redirect('service_type_data_handler')


# ---------------Service category views---------------

def service_category_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles displaying service_category list when the request type is GET and adding a new service_category when the request type is POST.

        Args:
            request: The incoming HTTP request. If GET, it shows the service_category list. If POST, it processes the logic for adding a new service_category.

        Returns:
            HttpResponse: For GET requests, it returns a response with the service_category list. For POST requests, if the user input is valid, it adds the 
            service_category and redirects to the main page. If the input is invalid, it renders the form with an error message and redirects to the main page.
    """
    try:

        if request.method == 'GET':

            page_obj = service_category_pagination(request)
            service_type = service_type_pagination(request)
            context = {
                'curl': admincurl,
                'page_obj': page_obj,
                'service_type': service_type
            }
            return render(request, 'service/service_category.html', context) 
        
        elif request.method == 'POST':

            form = AddServiceCategoryForm(request.POST)
            data = {
                'service_type': request.POST.get("service_type"),
                'service_category_name': request.POST.get("service_category_name"),
            }
            validate_service_category_details(data)

            if form.is_valid():

                form.save()
                page_obj = service_category_pagination(request)
                context = {
                    'curl': admincurl,
                    'page_obj': page_obj
                }
                messages.error(request, 'Added Successfully!!!')
                return redirect('service_category_data_handler')
        else:

            page_obj = service_category_pagination(request)
            service_type = service_type_pagination(request)
            context = {
                'curl': admincurl,
                'page_obj': page_obj,
                'service_type': service_type
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
    
    except Exception as e:
        messages.error(request, f"{e}")
        return redirect ( 'service_category_data_handler')

@csrf_exempt
def service_category_action_handler(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles updating service_category item when the request type is POST with an ID, and deleting service_category item when the request type is DELETE with an ID.

        Args:
            request: The incoming HTTP request. For POST requests, it updates the service_category specified by the ID in the request. For DELETE requests, it deletes the item specified by the ID.

        Returns:
            HttpResponse: For POST requests, if the update is successful, it redirects to the main page. If the update fails, it shows an error message and redirects to the main page. 
            For DELETE requests, if the deletion is successful, it redirects to the main page. If the deletion fails, it shows an error message and redirects to the main page.
    """
    try:
        if request.method == 'POST':
            servicecategory = ServiceCategory.objects.get(id=id)

            service_type = request.POST.get('service_type')
            service_category_name = request.POST.get('service_category_name')
            data = {
                'service_type': service_type,
                'service_category_name': service_category_name
            }
            validate_service_category_details(data)

            # Get old Details
            old_status = servicecategory.status
            old_service_category_name = servicecategory.service_category_name
            old_service_type = ServiceType.objects.get(id=int(servicecategory.service_type.id))

            # Update Details 
            servicecategory.status = request.POST.get('status', old_status)
            servicecategory.service_category_name = request.POST.get('service_category_name', old_service_category_name)
            servicecategory.service_type = ServiceType.objects.get(id=int(service_type)) if service_type else old_service_type
            servicecategory.save()


            messages.success(request, 'Updated successfully!')
            return redirect('service_category_data_handler')
        
        if request.method == 'DELETE':   
            servicecategory = ServiceCategory.objects.get(id=id)

            if servicecategory:
                servicecategory.delete()

                page_obj = service_category_pagination(request)
                context = {
                    'curl': admincurl,
                    'page_obj': page_obj
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
    
    except Exception as e:
        messages.error(request, f"Unexpected error occur, Try again")
        return redirect('service_category_data_handler')
 

# ---------------Services views---------------

@csrf_exempt
def service_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles displaying service list when the request type is GET and adding a new service when the request type is POST.

        Args:
            request: The incoming HTTP request. If GET, it shows the service list. If POST, it processes the logic for adding a new service.

        Returns:
            HttpResponse: For GET requests, it returns a response with the service list. For POST requests, if the user input is valid, it adds the 
            service and redirects to the main page. If the input is invalid, it renders the form with an error message and redirects to the main page.
    """
    try:
        if request.method == 'GET':

            page_obj = services_pagination(request)
            service_category = service_category_pagination(request)
            context = {
                'curl': admincurl,
                'page_obj': page_obj,
                'service_category': service_category
            }
            return render(request, 'service/services.html', context) 
        
        elif request.method == 'POST':

            form = AddServicsForm(request.POST)
            data = {
                'service_title': request.POST.get('service_title'),
                'service_category': request.POST.get('service_category'),
                'service_description': request.POST.get('service_description'),
            }
            validate_services_details(data)

            if form.is_valid():

                form.save()
                page_obj = services_pagination(request)
                context = {
                    'curl': admincurl,
                    'page_obj': page_obj
                }
                messages.success(request,"Added successfully!!!")
                return redirect('service_data_handler')
        else:

            page_obj = services_pagination(request)
            service_category = service_category_pagination(request)
            context = {
                'curl': admincurl,
                'page_obj': page_obj,
                'service_category': service_category
            }
            return render(request, 'service/services.html', context) 
            
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
    
    except Exception as e:
        messages.error(request, f"{e}")
        return redirect ( 'service_data_handler')
    
@csrf_exempt
def service_action_handler(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles updating service item when the request type is POST with an ID, and deleting service item when the request type is DELETE with an ID.

        Args:
            request: The incoming HTTP request. For POST requests, it updates the service specified by the ID in the request. For DELETE requests, it deletes the item specified by the ID.

        Returns:
            HttpResponse: For POST requests, if the update is successful, it redirects to the main page. If the update fails, it shows an error message and redirects to the main page. 
            For DELETE requests, if the deletion is successful, it redirects to the main page. If the deletion fails, it shows an error message and redirects to the main page.
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
            old_service_title = service.service_title
            old_service_description = service.service_description
            old_service_category = ServiceCategory.objects.get(id=int(service.service_category.id))

            # Update new or existing data
            service.status = request.POST.get('status', 1)
            service.service_title = request.POST.get('service_title', old_service_title)
            service.service_description = request.POST.get('service_description', old_service_description)
            service.service_category = ServiceCategory.objects.get(id=int(service_category)) if service_category else old_service_category
            service.save()

            messages.success(request, 'Update successfully!!')
            return redirect('service_data_handler')
        
        if request.method == 'DELETE':
            service = Services.objects.get(id=id)

            if service:
                service.delete()

                page_obj = services_pagination(request)
                service_category = service_category_pagination(request)
                context = {
                    'curl': admincurl,
                    'page_obj': page_obj,
                    'service_category': service_category
                }
                messages.success(request, 'Deleted successfully')
                return render(request, 'service/services.html', context)

            
            else:
                messages.error(request, f'This service is not found')
                return redirect('service_data_handler')
    
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.service_schema.services_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect ( 'service_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect ( 'service_data_handler')
        
    except ObjectDoesNotExist:
        messages.error(request ,f"Service category does not exist.")
        return redirect('service_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin_dashboard.html')

    except Exception as e:
        messages.error(request, f"{e}")
        return redirect('service_data_handler')

# ---------------Sub-services views---------------

@csrf_exempt
def sub_services_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles displaying sub_services list when the request type is GET and adding a new sub_services when the request type is POST.

        Args:
            request: The incoming HTTP request. If GET, it shows the sub_services list. If POST, it processes the logic for adding a new sub_services.

        Returns:
            HttpResponse: For GET requests, it returns a response with the sub_services list. For POST requests, if the user input is valid, it adds the 
            sub_services and redirects to the main page. If the input is invalid, it renders the form with an error message and redirects to the main page.
    """

    try:
        if request.method == 'GET':

            page_obj = sub_services_pagination(request)
            services = services_pagination(request)
            context = {
                'curl': admincurl,
                'page_obj': page_obj,
                'services': services
            }
            return render(request, 'service/sub_service.html',context)
        
        elif request.method == 'POST':
            form = AddSubServiceForm(request.POST)

            order = request.POST.get('order')
            service = request.POST.get('service')
            optional = request.POST.get('optional')
            display_text = request.POST.get('display_text')
            selection_type = request.POST.get('selection_type')
            sub_service_title = request.POST.get('sub_service_title')
            sub_service_description = request.POST.get('sub_service_description')

            data = {
                'status': "1",
                'order': order,
                'service': service,
                'optional': optional,
                'display_text': display_text,
                'selection_type': selection_type,
                'sub_service_title': sub_service_title,
                'sub_service_description': sub_service_description,
            }
            validate_sub_service_details(data)

            if form.is_valid():

                order = request.POST.get('order')
                service = request.POST.get('service')
                optional = request.POST.get('optional')
                selection_type = request.POST.get('selection_type')
                
                try:
                    data_validate = SubService.objects.get(service=service, order=order, selection_type=selection_type, optional=optional)

                except SubService.DoesNotExist:
                        form.save()
                        messages.success(request, 'Added Successful')
                        return redirect('sub_services_data_handler')
                
                except SubService.MultipleObjectsReturned:
                        messages.error(request, 'Same record already available, try again')
                        return redirect('sub_services_data_handler')
        else:
            page_obj = sub_services_pagination(request)
            services = services_pagination(request)
            context = {
                'curl': admincurl,
                'page_obj': page_obj,
                'services': services
            }
            return render(request, 'service/sub_service.html',context)
        
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.service_schema.sub_services_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect ( 'sub_services_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect ( 'sub_services_data_handler')
            
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin_dashboard.html')
    
    except Exception as e:
        messages.error(request, f"{e}")
        return redirect ( 'sub_services_data_handler')
    
@csrf_exempt
def sub_services_action_handler(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles updating sub_services item when the request type is POST with an ID, and deleting sub_services item when the request type is DELETE with an ID.

        Args:
            request: The incoming HTTP request. For POST requests, it updates the sub_services specified by the ID in the request. For DELETE requests, it deletes the item specified by the ID.

        Returns:
            HttpResponse: For POST requests, if the update is successful, it redirects to the main page. If the update fails, it shows an error message and redirects to the main page. 
            For DELETE requests, if the deletion is successful, it redirects to the main page. If the deletion fails, it shows an error message and redirects to the main page.
    """

    try:
        if request.method == 'POST':

            subservice = SubService.objects.get(id=id)
            order = request.POST.get('order')
            service = request.POST.get('service')
            optional = request.POST.get('optional')
            selection_type = request.POST.get('selection_type')

            data = {
                'order': order,
                'service': service,
                'optional': optional,
                'selection_type': selection_type,
                'status': request.POST.get('status'),
                'display_text': request.POST.get('display_text'),
                'sub_service_title': request.POST.get('sub_service_title'),
                'sub_service_description': request.POST.get('sub_service_description'),
            }
            validate_sub_service_details(data)           
            data_validate = SubService.objects.filter(service=service, order=order, selection_type=selection_type, optional=optional).count()

            if data_validate == 1:  

                # Update new or existing data
                subservice.order = request.POST.get('order',subservice.order)
                subservice.status = request.POST.get('status', subservice.status)
                subservice.optional = request.POST.get('optional', subservice.optional)
                subservice.display_text = request.POST.get('display_text',  subservice.display_text)
                subservice.selection_type = request.POST.get('selection_type', subservice.selection_type)
                subservice.sub_service_title = request.POST.get('sub_service_title', subservice.sub_service_title)
                subservice.sub_service_description = request.POST.get('sub_service_description', subservice.sub_service_description)
                subservice.service = Services.objects.get(id=int(service)) if service else Services.objects.get(id=int(subservice.service.id)) 
                subservice.save()

                messages.success(request, 'Update successfully!!')
                return redirect('sub_services_data_handler')
            
            elif data_validate > 1:
                messages.error(request, 'Same record already available, try again')
                return redirect('sub_services_data_handler')
            
        elif request.method == 'DELETE':
            sub_service = SubService.objects.get(id=id)

            if sub_service:
                sub_service.delete()

                page_obj = sub_services_pagination(request)
                services = services_pagination(request)
                context = {
                    'curl': admincurl,
                    'page_obj': page_obj,
                    'services': services
                }
                messages.success(request, 'Deleted successfully !')
                return render(request, 'service/sub_service.html', context)
            else:
                messages.error(request, 'this sub_service is nto found, try again')
                return redirect('sub_services_data_handler')

        else:
            messages.error(request, 'Invalid request, try again')
            return redirect('sub_services_data_handler')
    
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.service_schema.sub_services_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect ( 'sub_services_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect ( 'sub_services_data_handler')
    
    except ObjectDoesNotExist:
        messages.error(request ,f"Sub Service does not exist.")
        return redirect('sub_services_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin_dashboard.html')

    except Exception as e:
        messages.error(request, f"{e}")
        return redirect('sub_services_action_handler')
    
# ---------------Sub-services option views---------------

@csrf_exempt
def sub_service_option_data_handler(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles displaying sub_service_option list when the request type is GET and adding a new sub_service_option when the request type is POST.

        Args:
            request: The incoming HTTP request. If GET, it shows the sub_service_option list. If POST, it processes the logic for adding a new sub_service_option.

        Returns:
            HttpResponse: For GET requests, it returns a response with the sub_service_option list. For POST requests, if the user input is valid, it adds the 
            sub_service_option and redirects to the main page. If the input is invalid, it renders the form with an error message and redirects to the main page.
    """
    try:
        if request.method == 'GET':

            sub_service = sub_services_pagination(request)
            inspection = inspection_pagination(request)
            page_obj = sub_service_option_pagination(request)
            context = {
                'page_obj': page_obj,
                'inspection': inspection,
                'sub_service': sub_service,
            }

            return render(request,'service/sub_service_option.html', context)
        
        elif request.method == 'POST':

            option_type = request.POST.get('option_type')
            uploaded_file = request.FILES.get('option_image_url')
            form = AddSubServiceOptionForm(request.POST, request.FILES)

            image_format = (uploaded_file.name.split('.')[-1].lower() if option_type == "Image Type" and uploaded_file else "")

            data = {
                'option_type': option_type,
                'option_image': image_format,
                'order': request.POST.get('order'),
                'sub_service': request.POST.get('sub_service'),
                'option_title': request.POST.get('option_title'),
                }
            validate_sub_service_option_details(data)

            if form.is_valid():
                subServiceOption = form.save(commit=False)

                if uploaded_file:
                    image_name = uploaded_file.name
                    image_url = f'{media_path}/option_images/{image_name}' 
                    media_directory = os.path.join(settings.BASE_DIR, 'media/option_images')
                    file_path = os.path.join(media_directory, image_name)
                    subServiceOption.option_image_url = image_url
                    os.makedirs(media_directory, exist_ok=True)

                    with open(file_path, "wb") as fp:
                        for chunk in uploaded_file.chunks():
                            fp.write(chunk)

                subServiceOption.save()
                form.save_m2m()
                sub_service = sub_services_pagination(request)
                inspection = inspection_pagination(request)
                page_obj = sub_service_option_pagination(request)
                
                context = {
                    'page_obj': page_obj,
                    'inspection': inspection,
                    'sub_service': sub_service,
                }
                messages.success(request, 'Added successfully!')
                return render(request,'service/sub_service_option.html', context)
            
            else:
                messages.success(request, 'Form has not valid input')
                return render(request,'service/sub_service_option.html',)
        else:
            inspection = inspection_pagination(request)
            sub_service = sub_services_pagination(request)
            page_obj = sub_service_option_pagination(request)

            context = {
                'page_obj': page_obj,
                'inspection': inspection,
                'sub_service': sub_service,
            }
            return render(request,'service/sub_service_option.html', context)
        
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        print('test6')
        messages.error(request,schemas.service_schema.sub_services_option_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect ( 'sub_service_option_data_handler')
    
    except json.JSONDecodeError:
        print('test7')
        messages.error(request, f"{e}")
        return redirect ( 'sub_service_option_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin_dashboard.html')

    except Exception as e:
        messages.error(request, f"{e}")
        return redirect('sub_service_option_data_handler')
        
@csrf_exempt
def sub_service_option_action_handler(request: HttpRequest, id: int) -> HttpResponse | HttpResponseRedirect:
    """
    This method handles updating sub_service_option item when the request type is POST with an ID, and deleting sub_service_option item when the request type is DELETE with an ID.

        Args:
            request: The incoming HTTP request. For POST requests, it updates the sub_service_option specified by the ID in the request. For DELETE requests, it deletes the item specified by the ID.

        Returns:
            HttpResponse: For POST requests, if the update is successful, it redirects to the main page. If the update fails, it shows an error message and redirects to the main page. 
            For DELETE requests, if the deletion is successful, it redirects to the main page. If the deletion fails, it shows an error message and redirects to the main page.
    """
    try:
        if request.method == 'POST':

            sub_service = sub_services_pagination(request)
            inspection = inspection_pagination(request)
            page_obj = sub_service_option_pagination(request)

            context = {
                'page_obj': page_obj,
                'inspection': inspection,
                'sub_service': sub_service,
            }

            option_type = request.POST.get('option_type')
            uploaded_file = request.FILES.get('option_image_url')
            sub_service_option = SubServiceOption.objects.get(id=id)
            form = AddSubServiceOptionForm(request.POST, instance=sub_service_option)

            image_format = (uploaded_file.name.split('.')[-1].lower() if option_type == "Image Type" and uploaded_file else "")
            data = {
                'option_type': option_type,
                'option_image': image_format,
                'order': request.POST.get('order'),
                'sub_service': request.POST.get('sub_service'),
                'option_title': request.POST.get('option_title'),
                }
            validate_sub_service_option_details(data)

            if form.is_valid():
                update_option = form.save(commit=False)
                update_option.status = request.POST.get('status',1)

                if uploaded_file:
                    image_name = uploaded_file.name
                    image_url = f'{media_path}/option_images/{image_name}' 
                    media_directory = os.path.join(settings.BASE_DIR, 'media/option_images')
                    file_path = os.path.join(media_directory, image_name)
                    update_option.option_image_url = image_url
                    os.makedirs(media_directory, exist_ok=True)

                    with open(file_path, "wb") as fp:
                        for chunk in uploaded_file.chunks():
                            fp.write(chunk)

                update_option.option_image_url = "" if option_type == "Text Type" else update_option.option_image_url
                form.save()
                
                messages.error(request, "Updated successfully!")
                return redirect("sub_service_option_data_handler")
            
        elif request.method == 'DELETE':
            sub_service_option = SubServiceOption.objects.get(id=id)
            
            if sub_service_option:
                sub_service_option.delete()

                sub_service = sub_services_pagination(request)
                inspection = inspection_pagination(request)
                page_obj = sub_service_option_pagination(request)
                context = {
                    'page_obj': page_obj,
                    'inspection': inspection,
                    'sub_service': sub_service,
                }

                messages.success(request, "Deleted successfully!")
                return render(request, 'service/sub_service_option.html',context)
        else:
            messages.error(request, "In-valid request, try again")
            return redirect('sub_service_option_data_handler')
        
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        messages.error(request,schemas.service_schema.sub_services_option_schema.
        get('properties', {}).get(e.path[-1], {}).get('description', 'please enter the valid data'))
        return redirect ( 'sub_service_option_data_handler')
    
    except json.JSONDecodeError:
        messages.error(request, f"{e}")
        return redirect ( 'sub_service_option_data_handler')
    
    except ObjectDoesNotExist:
        messages.error(request ,f"Sub Service option does not exist.")
        return redirect('sub_service_option_data_handler')
    
    except TemplateDoesNotExist:
        messages.error(request, f"An unexpected error occurred. Please try again later.")
        return render(request, 'admin_dashboard.html')
    
    except Exception as e:
        messages.error(request, f"{e}")
        return redirect('sub_service_option_data_handler')