from django.db import models
from django.utils import timezone


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