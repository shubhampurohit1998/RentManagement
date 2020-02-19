# Generated by Django 3.0.3 on 2020-02-19 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0004_auto_20200218_0542'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Profile picture'),
        ),
        migrations.AlterField(
            model_name='picture',
            name='pic_name',
            field=models.ImageField(upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='property',
            name='address',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='property',
            name='city',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='property',
            name='description',
            field=models.TextField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='price',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='property',
            name='size',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='rent',
            name='date_on_rent',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='rent',
            name='tenure',
            field=models.DateField(blank=True, null=True),
        ),
    ]
