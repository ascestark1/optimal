from django.urls import path
from .views import *

urlpatterns = [
    path('subscribe/', newsletter_subscribe_view, name='newsletter_subscribe'),
    path('', index, name='index'),
    path('services/', services, name='services'),
    path('contact/', contact, name='contact'),
    path('booking/', booking, name='booking'),
    path('about/', about, name='about'),
    path('blog/', blog, name='blog'),
]