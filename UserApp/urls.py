from django.urls import path
from . import views

app_name = 'UserApp'
urlpatterns = [
    path('', views.register, name='register')
    # path('<int:ownr_id>/', views.index, name='index')
]