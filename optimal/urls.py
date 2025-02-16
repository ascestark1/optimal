from django.urls import path
from .views import *

urlpatterns = [
    path('subscribe/', newsletter_subscribe_view, name='newsletter_subscribe'),
    path('', index, name='index'),
    path('services/', services, name='services'),
    path('contact/', contact, name='contact'),
    path('booking/', booking, name='booking'),
    path('booking_package/<int:pk>/', booking_package, name='booking_package'),
    path('booking_success/', booking_success, name='booking_success'),
    path('about/', about, name='about'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('blog/', blog, name='blog'),
    path('blog_detail/', blog_detail, name='blog_detail'),
    path('approved_consultations/', approved_consultations, name='approved_consultations'),
    path('upcoming_consultations/', upcoming_consultations, name='upcoming_consultations'),
    path('client_list/', client_list, name='client_list'),
    path('wellness_packages/', wellness_packages, name='wellness_packages'),
    path('add_package/', add_package, name='add_package'),
    path('wellness_package_description/<int:pk>/', wellness_package_description, name='wellness_package_description'),
    path('packages_list/', package_list, name='package_list'),
    path('update_info/<int:pk>/', update_info, name='update_info'),
    path('edit_package/<int:pk>/', edit_package, name='edit_package'),
    path('payment_list/', payment_list, name='payment_list'),
    path('approved_payment_list/', approved_payment_list, name='approved_payment_list'),
    path('rejected_payment_list/', rejected_payment_list, name='rejected_payment_list'),



]