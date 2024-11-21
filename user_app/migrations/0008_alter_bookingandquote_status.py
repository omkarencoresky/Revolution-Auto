# Generated by Django 5.0.7 on 2024-10-30 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0007_subserviceandoption_service_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingandquote',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending for Quote', 'pending for quote'), ('Quoted', 'quoted'), ('Progressing', 'progressing'), ('Scheduled', 'scheduled'), ('Pending', 'pending'), ('Deleted', 'deleted'), ('Complete', 'complete'), ('Cancelled', 'cancelled')], default='pending for quote', max_length=50, null=True),
        ),
    ]
