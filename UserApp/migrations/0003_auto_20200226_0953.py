# Generated by Django 3.0.3 on 2020-02-26 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0002_auto_20200226_0613'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_customer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_owner',
            field=models.BooleanField(default=False),
        ),
    ]
