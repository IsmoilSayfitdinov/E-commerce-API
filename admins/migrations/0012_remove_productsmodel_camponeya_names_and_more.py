# Generated by Django 5.0.6 on 2024-08-01 15:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0011_alter_productsmodel_subcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productsmodel',
            name='camponeya_names',
        ),
        migrations.AddField(
            model_name='productsmodel',
            name='camponeya_names',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admins.camponeyanames'),
        ),
    ]
