# Generated by Django 5.0.7 on 2024-11-19 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0017_service_payment_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service_payment',
            name='status',
            field=models.CharField(default='pending', max_length=200),
        ),
    ]
