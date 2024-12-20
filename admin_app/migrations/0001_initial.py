# Generated by Django 5.0.7 on 2024-10-24 09:04

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarBrand',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('brand', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, max_length=2000)),
                ('image_url', models.ImageField(upload_to='brand_images/')),
                ('status', models.SmallIntegerField(default=1)),
                ('remember_token', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'car_brand',
            },
        ),
        migrations.CreateModel(
            name='Inspection',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('inspection_name', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'inspection',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('location_name', models.CharField(max_length=150)),
                ('country_code', models.CharField(max_length=50)),
                ('service_availability', models.BooleanField(default=True)),
                ('status', models.SmallIntegerField(default=1)),
                ('remember_token', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'location',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('recipient_type', models.CharField(choices=[('user', 'user'), ('mechanic', 'mechanic'), ('admin', 'admin')], default=1, max_length=20)),
                ('title', models.CharField(max_length=255)),
                ('email_status', models.CharField(choices=[('Sent', 'sent'), ('Failed', 'failed')], default='complete', max_length=20)),
                ('message', models.TextField(blank=True, max_length=5000)),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'notification',
            },
        ),
        migrations.CreateModel(
            name='ServiceCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('service_category_name', models.CharField(max_length=150)),
                ('status', models.SmallIntegerField(default=1)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'service_category',
            },
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('service_title', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True, max_length=5000)),
                ('status', models.SmallIntegerField(default=1)),
                ('is_popular', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=5)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'service',
            },
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('service_type_name', models.CharField(max_length=150)),
                ('status', models.SmallIntegerField(default=1)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'service_type',
            },
        ),
        migrations.CreateModel(
            name='SubService',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('order', models.SmallIntegerField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.SmallIntegerField(default=1)),
                ('display_text', models.CharField(blank=True, max_length=200)),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True, max_length=5000)),
                ('optional', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5)),
                ('selection_type', models.CharField(choices=[('Single', 'Single'), ('Multiple', 'Multiple')], max_length=8)),
            ],
            options={
                'db_table': 'sub_service',
            },
        ),
        migrations.CreateModel(
            name='SubServiceOption',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('order', models.SmallIntegerField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.SmallIntegerField(default=1)),
                ('description', models.TextField(blank=True, max_length=5000)),
                ('image_url', models.ImageField(blank=True, null=True, upload_to='media/option_images')),
                ('option_type', models.CharField(choices=[('Text Type', 'Text Type'), ('Image Type', 'Image Type')], max_length=20)),
            ],
            options={
                'db_table': 'sub_service_option',
            },
        ),
        migrations.CreateModel(
            name='UserReferral',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('referred_email', models.EmailField(max_length=255)),
                ('booking_id', models.CharField(blank=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('referred_register_status', models.BooleanField(default=False)),
                ('redeem_status', models.CharField(choices=[('Redeemed', 'redeemed'), ('Available', 'available')], default='available', max_length=20)),
            ],
            options={
                'db_table': 'user_referral',
            },
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('model_name', models.CharField(max_length=50)),
                ('status', models.SmallIntegerField(default=1)),
                ('remember_token', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('car_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.carbrand')),
            ],
            options={
                'db_table': 'car_model',
            },
        ),
        migrations.CreateModel(
            name='CarYear',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('year', models.CharField(max_length=6)),
                ('status', models.SmallIntegerField(default=1)),
                ('remember_token', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('car_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.carbrand')),
            ],
            options={
                'db_table': 'car_year',
            },
        ),
        migrations.CreateModel(
            name='CarTrim',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('car_trim_name', models.CharField(max_length=100)),
                ('status', models.SmallIntegerField(default=1)),
                ('remember_token', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('car_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.carbrand')),
                ('model_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.carmodel')),
                ('year_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.caryear')),
            ],
            options={
                'db_table': 'car_trim',
            },
        ),
        migrations.AddField(
            model_name='carmodel',
            name='year_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.caryear'),
        ),
    ]
