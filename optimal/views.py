from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.utils.timezone import now
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient
from .forms import WellnessPackageForm

def index(request):
    return render(request, 'index.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contact.html')

def wellness_packages(request):
    men_wellness = WellnessPackage.objects.filter(category__name="Men Wellness")
    women_wellness = WellnessPackage.objects.filter(category__name="Women Wellness")
    family_wellness = WellnessPackage.objects.filter(category__name="Family Wellness")
    senior_wellness = WellnessPackage.objects.filter(category__name="Senior Wellness")
    other_wellness = WellnessPackage.objects.filter(category__name="Other Wellness")


    context = {
        'men_wellness': men_wellness,
        'women_wellness': women_wellness,
        'family_wellness': family_wellness,
        'other_wellness':  other_wellness,
    }

    return render(request, 'wellness_packages.html', context)

def wellness_package_description(request, pk):
    package = get_object_or_404(WellnessPackage, pk=pk)
    return render(request, 'wellness_package_description.html', {'package':package} )


def contact(request):
    return render(request, 'contact.html')

def admin_dashboard(request):
     # Fetch all records from the ConsultationBooking model
    consultations = ConsultationBooking.objects.all()
    context = {
        'consultations': consultations
    }
    return render(request, 'adminstrator/dashboard.html', context)


def client_list(request):
    # Fetch all records from the ConsultationBooking model, ordered by latest first
    consultations = ConsultationBooking.objects.filter(is_payment_verified='Pending').order_by('-consultation_date')
    context = {
        'consultations': consultations
    }
    return render(request, 'adminstrator/clients_list.html', context)

def payment_list(request):
    # Fetch all records from the ConsultationBooking model, ordered by latest first
    payments = Payment.objects.all().order_by('-created_at')  # Fetch payments in latest order

    context = {
        'payments': payments
    }
    return render(request, 'adminstrator/payment_list.html', context)


def approved_consultations(request):
    # Fetch only records where payment is verified
    consultations = ConsultationBooking.objects.filter(is_payment_verified='Paid')
    context = {
        'consultations': consultations
    }
    return render(request, 'adminstrator/clients_list.html', context)

def upcoming_consultations(request):
    # Fetch consultations with dates in the future
    consultations = ConsultationBooking.objects.filter(consultation_date__gte=now()).order_by('consultation_date')
    context = {
        'consultations': consultations
    }
    return render(request, 'adminstrator/clients_list.html', context)

def about(request):
    return render(request, 'about.html')


def booking_success(request):
    return render(request, 'success.html')

def blog(request):
    return render(request, 'blog.html')

def blog_detail(request):
    return render(request, 'blog_detail.html')


def approved_payment_list(request):
    # Fetch only successful payments, ordered by latest first
    payments = Payment.objects.filter(status='success').order_by('-created_at')

    context = {
        'payments': payments
    }
    return render(request, 'adminstrator/payment_list.html', context)


def rejected_payment_list(request):
    # Fetch only successful payments, ordered by latest first
    payments = Payment.objects.filter(status='failed').order_by('-created_at')

    context = {
        'payments': payments
    }
    return render(request, 'adminstrator/payment_list.html', context)



def update_info(request, pk):
    booking = get_object_or_404(ConsultationBooking, id=pk)

    if request.method == "POST":
        booking.full_name = request.POST.get("full_name")
        booking.email = request.POST.get("email")
        booking.residence = request.POST.get("residence")
        booking.phone_number = request.POST.get("phone_number")
        booking.patient_consulting = request.POST.get("patient_consulting")
        booking.patient_relationship = request.POST.get("patient_relationship")
        booking.consultation_date = request.POST.get("consultation_date")
        booking.description = request.POST.get("description")
        booking.is_payment_verified = request.POST.get("is_payment_verified")
        booking.zoom_link = request.POST.get("zoom_link")

        booking.save()
        return redirect(client_list)  # Redirect after update

    return render(request, "adminstrator/update_info.html", {"booking": booking})

    return render(request, '')

def add_package(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = WellnessPackageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('package_list')  # Redirect to package list after saving
    else:
        form = WellnessPackageForm()

    return render(request, 'adminstrator/add_package.html', {'form': form, 'categories': categories})    

def process_payment(phone_number, amount, account_reference, transaction_desc):
    cl = MpesaClient()
    callback_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

    return response
   




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
        residence = request.POST.get('residence')
        phone_number = request.POST.get('phone_number')
        patient_consulting = request.POST.get('patient_consulting')
        patient_relationship = request.POST.get('patient_relationship')
        consultation_date = request.POST.get('consultation_date')
        transaction_desc = request.POST.get('description')
        account_reference = full_name + phone_number
        consultation = ConsultationBooking(
            full_name=full_name,
            email=email,
            residence=residence,
            phone_number=phone_number,
            patient_consulting=patient_consulting,
            patient_relationship=patient_relationship,
            consultation_date=consultation_date,
            description=transaction_desc
        )
        
        consultation.save()
        payment = Payment.objects.create(
        phone_number=phone_number,
        amount=1000,
        account_reference=account_reference,
        transaction_desc=transaction_desc,
        status="pending"
    )
        response = process_payment(phone_number, 1000, account_reference, transaction_desc)
        print(response)
        return redirect('booking_success')
       
    return render(request, 'booking.html', {'error': 'All fields are required'})
    
    return render(request, 'booking.html')


def package_list(request):
    packages = WellnessPackage.objects.all()
    return render(request, 'adminstrator/packages_list.html', {'packages': packages})


def edit_package(request, pk):
    package = get_object_or_404(WellnessPackage, id=pk)
    
    if request.method == 'POST':
        form = WellnessPackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            return redirect('package_list')  # Redirect to package list or details page
    else:
        form = WellnessPackageForm(instance=package)

    return render(request, 'adminstrator/edit_package.html', {'form': form, 'package': package})


def booking_package(request, pk):
    package = get_object_or_404(WellnessPackage, pk=pk)
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        residence = request.POST.get('residence')
        phone_number = request.POST.get('phone_number')
        patient_consulting = request.POST.get('patient_consulting')
        patient_relationship = request.POST.get('patient_relationship')
        consultation_date = request.POST.get('consultation_date')
        transaction_desc = request.POST.get('description')
        price = int(float(request.POST.get('price')))
        account_reference = full_name + phone_number
        consultation = ConsultationBooking(
            full_name=full_name,
            email=email,
            residence=residence,
            phone_number=phone_number,
            patient_consulting=patient_consulting,
            patient_relationship=patient_relationship,
            consultation_date=consultation_date,
            description=transaction_desc
        )
        
        consultation.save()
        payment = Payment.objects.create(
        phone_number=phone_number,
        amount=price,
        account_reference=account_reference,
        transaction_desc=transaction_desc,
        status="pending"
    )
        response = process_payment(phone_number, price, account_reference, transaction_desc)
        print(response)
        return redirect('booking_success')
       
    return render(request, 'booking_package.html', {'error': 'All fields are required', 'package': package})
    
    return render(request, 'booking_package.html',  {'packages': packages})
