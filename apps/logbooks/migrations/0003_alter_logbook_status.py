# Generated by Django 5.2 on 2025-06-13 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logbooks', '0002_logbook_unique_logbook_per_internship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logbook',
            name='status',
            field=models.CharField(choices=[('approved', 'Approved'), ('rejected', 'Rejected'), ('pending_approval', 'Pending Approval')], default='pending_approval'),
        ),
    ]
