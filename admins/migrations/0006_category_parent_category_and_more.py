# Generated by Django 5.0.6 on 2024-07-25 15:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0005_productsmodel_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='parent_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admins.category'),
        ),
        migrations.RemoveField(
            model_name='productsmodel',
            name='category',
        ),
        migrations.AddField(
            model_name='productsmodel',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='admins.category'),
            preserve_default=False,
        ),
    ]
