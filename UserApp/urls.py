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
    path('add-profile-picture/<int:person_id>', views.add_profile_picture, name='add_profile_picture'),
    path('leave-request/<int:property_id>', views.leave_request, name='leave_request'),
    path('owner-leave-panel/', views.leave_request_panel, name='owner_leave_panel'),
    path('request-accept/<int:request_id>', views.leave_request_accept, name='request_accept'),
    path('request-cancel/<int:request_id>', views.leave_request_cancel, name='request_cancel'),
]
