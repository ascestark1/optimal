from django.db import models
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.views import View

# Models
class NewsletterSubscriber(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.full_name

class ConsultationBooking(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    consultation_date = models.DateTimeField()
    message = models.CharField(max_length=1000)
    is_payment_verified = models.BooleanField(default=False)
    zoom_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Booking by {self.full_name} on {self.consultation_date}"
