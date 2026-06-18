from django.urls import path
from . import views

urlpatterns = [
    # Base URL
    path('', views.home, name="home"),
    
    # Main pages
    path('store/', views.store, name="store"),
    path('rent/', views.rent, name="rent"),
    path('sell/', views.sell, name="sell"),
    path('car_maintenance/', views.car_maintenance, name="car_maintenance"),
    path('privacy/', views.privacy, name="privacy"),
    path('termsandcondition/', views.termsandcondition, name="termsandcondition"),
    path('disclaimer/', views.disclaimer, name="disclaimer"),

    # Form submission and success
    path('contact_form_submit/', views.contact_form_submit, name='contact_form_submit'),
    path('submit-interest/', views.submit_interest, name='submit-interest'),
    path('submit-rent-interest/', views.submit_rent_interest, name='submit-rent-interest'),
    path('submit-sell-interest/', views.submit_sell_interest, name='submit-sell-interest'),
    path('success/', views.success_view, name='success'),  # Ensure you have a success view
    
    # Other actions
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),

    #Views more images
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('submit-interest/', views.submit_interest, name='submit_interest'),


    path('', views.rent_list, name='rent_list'),
    path('rent/<int:rent_id>/', views.rent_detail, name='rent_detail'),

    path('wishlist/', views.add_to_wishlist, name='wishlist'),
]
