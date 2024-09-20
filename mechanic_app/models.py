from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password

# Create your models here.


class Mechanic(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=225, unique=True, blank=False)
    phone_no = models.CharField(max_length=20, blank=False)
    status = models.SmallIntegerField(default=1, blank=False)
    approved = models.SmallIntegerField(default=0, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)
    password = models.CharField(max_length=128, blank=False)
    profile_image = models.ImageField(upload_to='mechanic_images/', default=0)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    class Meta:
        db_table = 'mechanic'
