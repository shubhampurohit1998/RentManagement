from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='home'),
    path('add-property/', views.add_property, name='register_property'),
    path('property-list/', views.show_property_list, name='show_property'),
    path('add-image/<int:property_id>', views.add_property_images, name='add_image'),
    path('delete-property/<int:property_id>', views.delete_property, name='delete_property'),
    path('update-property/<int:property_id>', views.update_property_details, name='update_property'),
    path('view-details/<int:property_id>', views.property_detail, name='view_details'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('update-profile/', views.update_user_profile, name='update_profile'),
    path('time-period/<int:property_id>', views.property_on_rent, name='time_period'),
    path('rental-assets/', views.rental_property_list, name='rental_assets'),
    path('delete-image/<int:image_id>', views.delete_property_image, name='delete_image'),
    path('renter-details/<int:property_id>', views.renter_details, name='renter_details'),
    path('properties/', views.search_random_properties, name='random_properties'),
    path('user-list/', views.UserList.as_view(), name='user_list'),
    path('user-detail/', views.UserDetail.as_view(), name='user_detail'),
    path('add-profile-picture/<int:person_id>', views.add_profile_picture, name='add_profile_picture')
]
