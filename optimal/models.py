from django.db import models
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.views import View
import uuid
# Models
class NewsletterSubscriber(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.full_name

class ConsultationBooking(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Rejected', 'Rejected'),
    ]
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    residence = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=15, unique=True)
    patient_consulting = models.CharField(max_length=255)
    patient_relationship = models.CharField(max_length=255)
    consultation_date = models.DateTimeField()
    description = models.CharField(max_length=1000)
    is_payment_verified = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default='Pending'
    )
    zoom_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Booking by {self.full_name} on {self.consultation_date}"


class Payment(models.Model):
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account_reference = models.CharField(max_length=100)
    transaction_desc = models.TextField()
    transaction_id = models.CharField(max_length=100, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')])
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.transaction_id:  # Only generate if transaction_id is empty
            self.transaction_id = f"TXN-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.phone_number} - {self.status}"


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class WellnessPackage(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='packages/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='packages')

    def __str__(self):
        return self.title
    
    def get_description_list(self):
        return self.description.split("\n") 

def approved_payment_list(request):
    # Fetch only successful payments, ordered by latest first
    payments = Payment.objects.filter(status='success').order_by('-created_at')

    context = {
        'payments': payments
    }
    return render(request, 'adminstrator/payment_list.html', context)
