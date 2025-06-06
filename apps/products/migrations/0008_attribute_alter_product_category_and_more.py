# Generated by Django 5.2 on 2025-05-27 14:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0007_product_image_delete_productimage"),
    ]

    operations = [
        migrations.CreateModel(
            name="Attribute",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("color", models.CharField(max_length=100)),
                ("size", models.SlugField(unique=True)),
                ("material", models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products_category",
                to="products.category",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="attributes",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products_attributes",
                to="products.attribute",
            ),
        ),
    ]
