from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('add-property/', views.add_property, name='register_property'),
    path('property-list/', views.show_property_list, name='show_property'),
    path('add-image/<int:property_id>', views.add_property_images, name='add_image'),
    path('delete-property/<int:property_id>', views.delete_property, name='delete_property'),
    path('update-property/<int:property_id>', views.update_property_details, name='update_property'),
    path('view-details/<int:property_id>', views.property_detail, name='view_details'),
    path('profile', views.profile, name='profile'),
    path('update-profile/', views.update_user_profile, name='update_profile'),
    path('time-period/<int:property_id>', views.property_on_rent, name='time_period'),
]
