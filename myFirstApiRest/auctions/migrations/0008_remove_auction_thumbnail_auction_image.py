# Generated by Django 4.2.20 on 2025-05-11 18:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0007_comment"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="auction",
            name="thumbnail",
        ),
        migrations.AddField(
            model_name="auction",
            name="image",
            field=models.ImageField(default="images/default.webp", upload_to="images"),
        ),
    ]
