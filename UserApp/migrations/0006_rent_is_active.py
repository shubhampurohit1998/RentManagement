# Generated by Django 3.0.3 on 2020-02-27 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0005_auto_20200227_0727'),
    ]

    operations = [
        migrations.AddField(
            model_name='rent',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
