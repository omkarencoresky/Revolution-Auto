# Generated by Django 5.0.7 on 2024-09-03 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0012_inspection_rename_subservices_subservice_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subserviceoption',
            name='option_image',
            field=models.ImageField(blank=True, null=True, upload_to='media/option_images'),
        ),
    ]
