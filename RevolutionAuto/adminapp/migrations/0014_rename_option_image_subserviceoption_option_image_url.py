# Generated by Django 5.0.7 on 2024-09-03 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0013_subserviceoption_option_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subserviceoption',
            old_name='option_image',
            new_name='option_image_url',
        ),
    ]
