# Generated by Django 4.1 on 2025-02-27 08:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("farmer", "0009_payment"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="cat",
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="product",
            name="qty",
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
