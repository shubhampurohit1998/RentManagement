# Generated by Django 3.0.3 on 2020-03-02 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0007_auto_20200227_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.TextField(default=1, max_length=150),
            preserve_default=False,
        ),
    ]