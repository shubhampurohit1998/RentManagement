from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Owner)
admin.site.register(Customer)
admin.site.register(Property)
admin.site.register(Rent)

