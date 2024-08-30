from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field


# Car management Models
class CarBrand(models.Model):
    id = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=200, blank=True)
    image_url = models.ImageField(  upload_to='media/')
    status = models.SmallIntegerField(blank=False, default=1)
    remember_token = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table ='car_brand'

class CarYear(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.CharField(max_length=6,blank=False)
    car_id = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    status = models.SmallIntegerField(blank=False, default=1)
    remember_token = models.CharField(max_length=100,blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'car_year'

class CarModel(models.Model):
    id = models.AutoField(primary_key=True)
    car_id = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    year_id = models.ForeignKey(CarYear, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=50, blank=False)
    status = models.SmallIntegerField(blank=False,default=1)
    remember_token = models.CharField(max_length=100,blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'car_model'

class CarTrim(models.Model):
    id = models.AutoField(primary_key=True)
    car_id = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    year_id = models.ForeignKey(CarYear, on_delete=models.CASCADE)
    model_id = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    car_trim_name = models.CharField(max_length=100, blank=False)
    status = models.SmallIntegerField(blank=False,default=1)
    remember_token = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'car_trim'


# Location Models
class Location(models.Model):
    id = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=150, blank=False)
    country_code = models.CharField(max_length=50, blank=False)
    service_availability = models.BooleanField(default=True, blank=False)
    status = models.SmallIntegerField(default=1, blank=False)
    remember_token = models.CharField(max_length=100, blank=True) # Remove it next make migration
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'location'


# Service Models
class ServiceType(models.Model):
    id = models.AutoField(primary_key=True)
    service_type_name = models.CharField(max_length=150, blank=False)
    status = models.SmallIntegerField(default=1, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'service_type'

class ServiceCategory(models.Model):
    id = models.AutoField(primary_key=True)
    service_category_name = models.CharField(max_length=150, blank=False)
    service_type = models.ForeignKey(ServiceType,on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=1, blank=False)
    # remember_token = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'service_category'

class Services(models.Model): #Add a column for the popularityof services
    YES_NO_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    id = models.AutoField(primary_key=True)
    service_title = models.CharField(max_length=150, blank=False)
    service_description = CKEditor5Field('Content', config_name='extends')
    service_category = models.ForeignKey(ServiceCategory,on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=1, blank=False)
    is_popular = models.CharField(max_length=5, choices=YES_NO_CHOICES, default='No' ) 
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'services'


class SubServices(models.Model):
    YES_NO_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    SELECTION_TYPE_CHOICES = [
        ('Single', 'Single'),
        ('Multiple', 'Multiple'),
    ]

    id = models.AutoField(primary_key=True)
    sub_service_title = models.CharField(max_length=150, blank=False)
    sub_service_description = CKEditor5Field('Content', config_name='extends')
    service = models.ForeignKey(Services,on_delete=models.CASCADE)
    selection_type = models.CharField(max_length=8, choices=SELECTION_TYPE_CHOICES, default='No' ) 
    order = models.SmallIntegerField(blank=False)
    optional = models.CharField(max_length=5, choices=YES_NO_CHOICES, default='No' ) 
    status = models.SmallIntegerField(default=1, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sub_services'

