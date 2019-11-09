from django.contrib import admin

from .models import (Address, Conversation, Message, TextMessage, Patient, Therapist,
                     User, Device, PaymentProfile, Payment, Card, Bank, AppointmentRequestMessage,
                     PaymentProfile, Review, Appointment, AppointmentRequest, Area, Injury,
                     TherapistCertification, AppointmentCancellation)


class AppointmentCancellationAdmin(admin.ModelAdmin):
  readonly_fields = ('cancellation_time',)

admin.site.register(User)
admin.site.register(Address)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(TextMessage)
admin.site.register(Therapist)
admin.site.register(Patient)
admin.site.register(Device)
admin.site.register(Bank)
admin.site.register(Card)
admin.site.register(Payment)
admin.site.register(PaymentProfile)
admin.site.register(Appointment)
admin.site.register(AppointmentCancellation, AppointmentCancellationAdmin)
admin.site.register(AppointmentRequest)
admin.site.register(AppointmentRequestMessage)
admin.site.register(Review)
admin.site.register(Injury)
admin.site.register(TherapistCertification)
admin.site.register(Area)

