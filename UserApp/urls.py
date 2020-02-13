from django.urls import path
from . import views

app_name = 'UserApp'
urlpatterns = [
    path('', views.index, name='home'),
]
