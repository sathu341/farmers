# Generated by Django 5.1.6 on 2025-03-04 09:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("farmer", "0012_shop_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newcart",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="farmer.shop"
            ),
        ),
    ]
