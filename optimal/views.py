from django.shortcuts import render, redirect
from .models import *

def index(request):
    return render(request, 'index.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contact.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def blog(request):
    return render(request, 'blog.html')




def newsletter_subscribe_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        if full_name and email and phone_number:
            NewsletterSubscriber.objects.create(
                full_name=full_name, email=email, phone_number=phone_number
            )
            return redirect('newsletter_success')
        else:
            return render(request, 'newsletter_subscribe.html', {'error': 'All fields are required'})
    
    return render(request, 'newsletter_subscribe.html')

def booking(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('number')
        consultation_date = request.POST.get('consultation_date')
        message = request.POST.get('message')

        if full_name and email and phone_number and consultation_date and message:
            ConsultationBooking.objects.create(
                full_name=full_name, email=email, phone_number=phone_number, consultation_date=consultation_date, message=message
            ) 
            return redirect('booking_success')
        else:
            return render(request, 'booking.html', {'error': 'All fields are required'})
    
    return render(request, 'booking.html')
