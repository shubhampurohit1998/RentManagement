# Generated by Django 3.0.3 on 2020-02-27 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0006_rent_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserApp.Property'),
        ),
    ]
