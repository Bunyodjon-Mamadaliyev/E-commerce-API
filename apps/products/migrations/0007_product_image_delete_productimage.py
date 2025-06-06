# Generated by Django 5.2 on 2025-05-27 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "products",
            "0006_remove_product_thumbnail_product_attributes_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="products/"
            ),
        ),
        migrations.DeleteModel(
            name="ProductImage",
        ),
    ]
