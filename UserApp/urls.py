from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('add-property/', views.add_property, name='register_property'),
    path('property-list/', views.show_property_list, name='show_property'),
    path('add-images/<int:property_id>', views.add_property_images, name='add_image'),

]
