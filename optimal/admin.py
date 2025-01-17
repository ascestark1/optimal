from django.contrib import admin
from .models import *

@admin.action(description="Verify payment and send Zoom link")
def verify_payment_and_send_zoom_link(modeladmin, request, queryset):
    for booking in queryset:
        if not booking.is_payment_verified:
            booking.is_payment_verified = True
            booking.zoom_link = "https://zoom.us/your-meeting-link"  # Example link
            booking.save()

            # Send email to user
            send_mail(
                subject="Consultation Confirmation",
                message=f"Your consultation is confirmed. Join using this Zoom link: {booking.zoom_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[booking.email],
            )

class ConsultationBookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'consultation_date', 'is_payment_verified')
    actions = [verify_payment_and_send_zoom_link]

admin.site.register(NewsletterSubscriber)
admin.site.register(ConsultationBooking, ConsultationBookingAdmin)
