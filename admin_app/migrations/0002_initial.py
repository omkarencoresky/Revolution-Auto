# Generated by Django 5.0.7 on 2024-10-24 09:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admin_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='recipient_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipient_name', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notification',
            name='sender_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_name', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='services',
            name='service_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.servicecategory'),
        ),
        migrations.AddField(
            model_name='servicecategory',
            name='service_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.servicetype'),
        ),
        migrations.AddField(
            model_name='subservice',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.services'),
        ),
        migrations.AddField(
            model_name='subserviceoption',
            name='next_sub_service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_sub_service_options', to='admin_app.subservice'),
        ),
        migrations.AddField(
            model_name='subserviceoption',
            name='recommend_inspection_service',
            field=models.ManyToManyField(blank=True, to='admin_app.inspection'),
        ),
        migrations.AddField(
            model_name='subserviceoption',
            name='sub_service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_service_option', to='admin_app.subservice'),
        ),
        migrations.AddField(
            model_name='userreferral',
            name='referrer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refer_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
