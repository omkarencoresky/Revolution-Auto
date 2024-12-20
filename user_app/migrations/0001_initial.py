# Generated by Django 5.0.7 on 2024-10-24 09:04

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admin_app', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('phone_no', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.SmallIntegerField(default=1)),
                ('last_name', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('approved', models.SmallIntegerField(default=1)),
                ('role', models.CharField(choices=[('user', 'user'), ('admin', 'admin'), ('superadmin', 'superadmin'), ('mechanic', 'mechanic')], default='user', max_length=20)),
                ('profile_image', models.ImageField(default=0, upload_to='profile_images/')),
                ('remember_token', models.CharField(editable=False, max_length=100, unique=True)),
                ('groups', models.ManyToManyField(blank=True, related_name='customuser_groups', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='customuser_permissions', to='auth.permission')),
            ],
            options={
                'verbose_name': 'Custom User',
                'verbose_name_plural': 'Custom Users',
                'db_table': 'custom_user',
            },
        ),
        migrations.CreateModel(
            name='BookingAndQuote',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('car_services', models.JSONField()),
                ('car_sub_service', models.JSONField()),
                ('status', models.CharField(choices=[('Pending for Quote', 'pending for quote'), ('Quoted', 'quoted'), ('Progressing', 'progressing'), ('Scheduled', 'scheduled'), ('Pending', 'pending'), ('Deleted', 'deleted'), ('Complete', 'complete'), ('Cancelled', 'cancelled')], default='pending for quote', max_length=50)),
                ('total_service_amount', models.IntegerField(null=True)),
                ('parts_amount', models.IntegerField(null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('schedule_at', models.DateField(blank=True, null=True)),
                ('schedule_time_slot', models.TimeField(blank=True, null=True)),
                ('car_brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_car_brand', to='admin_app.carbrand')),
                ('car_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_car_model', to='admin_app.carmodel')),
                ('car_service_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_service_category', to='admin_app.servicecategory')),
                ('car_service_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_service_type', to='admin_app.servicetype')),
                ('car_trim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_car_trim', to='admin_app.cartrim')),
                ('car_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_car_year', to='admin_app.caryear')),
                ('mechanic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assign_mechanic', to=settings.AUTH_USER_MODEL)),
                ('service_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_location', to='admin_app.location')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_service', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'booking',
            },
        ),
        migrations.CreateModel(
            name='UserCarRecord',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('vin_number', models.CharField(blank=True, max_length=16)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('car_brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_details', to='admin_app.carbrand')),
                ('car_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cardetails', to='admin_app.carmodel')),
                ('car_trim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_details', to='admin_app.cartrim')),
                ('car_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_details', to='admin_app.caryear')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_details', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_car_record',
            },
        ),
    ]
