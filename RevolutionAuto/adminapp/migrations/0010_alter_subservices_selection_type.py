# Generated by Django 5.0.7 on 2024-09-02 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0009_subservices_display_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subservices',
            name='selection_type',
            field=models.CharField(choices=[('Single', 'Single'), ('Multiple', 'Multiple')], default='Multiple', max_length=8),
        ),
    ]
