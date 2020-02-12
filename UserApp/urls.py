from django.urls import path

from . import views
from .models import *
app_name = 'UserApp'
urlpatterns = [
    path('<int:ownr_id>/', views.index, name='index')
]