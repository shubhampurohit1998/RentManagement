# Generated by Django 3.0.3 on 2020-02-19 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0006_auto_20200219_0645'),
    ]

    operations = [
        migrations.AddField(
            model_name='rent',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
