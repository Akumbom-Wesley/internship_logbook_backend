# Generated by Django 5.2 on 2025-04-29 11:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('evaluation_categories', '0001_initial'),
        ('evaluations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluationcategory',
            name='evaluation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='evaluations.evaluation'),
        ),
    ]
