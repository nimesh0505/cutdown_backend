# Generated by Django 4.0.5 on 2022-06-18 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("urlshortner", "0004_rename_cutdownurl_shortenurl"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shortenurl",
            name="origin_url",
            field=models.CharField(max_length=1000000),
        ),
    ]
