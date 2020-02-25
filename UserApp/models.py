# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser
from idna import unicode


class User(AbstractUser):
    mobile = models.CharField(max_length=10, blank=True, null=True, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/',
                                        blank=True, null=True, verbose_name='Profile picture')
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.first_name


class Property(models.Model):
    PROPERTY_TYPE = [
        ('office', 'Office'),
        ('home', 'Home'),
        ('flat', 'Flat'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.CharField(max_length=30,)
    size = models.CharField(max_length=30,)
    address = models.CharField(max_length=100,)
    p_type = models.CharField(
        max_length=8,
        choices=PROPERTY_TYPE,
    )
    city = models.CharField(max_length=30, null=False, blank=False,)
    description = models.TextField(max_length=150, blank=True, null=True,)
    is_active = models.BooleanField(default=True, )

    class Meta:
        get_latest_by = id

    def __str__(self):
        return unicode(self.city)  # f-string python 3 string concatenation


class Rent(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    date_on_rent = models.DateField(null=False,)
    tenure = models.DateField(blank=True, null=True,)

    def __str__(self):
        return unicode(self.property)


class Picture(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    pic_name = models.ImageField(upload_to='images/')


class Message(models.Model):
    message = models.TextField(max_length=150, blank=True, null=True)
    rent = models.ForeignKey(Rent, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.rent.id
class LeaveRequest(models.Model):
    pass