# Generated by Django 5.0.7 on 2024-08-28 06:59

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0006_alter_services_service_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='service_description',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Content'),
        ),
    ]
