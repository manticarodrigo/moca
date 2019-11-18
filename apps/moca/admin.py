from django.contrib import admin

from .models import (Address, Conversation, Message, TextMessage, Patient, Therapist, AwayPeriod,
                     User, Device, Payment, Card, Bank, Price, AppointmentRequestMessage,
                     PaymentProfile, Review, Appointment, AppointmentRequest, AvailableArea,
                     Certification, CertificationImage, Injury, InjuryImage,
                     AppointmentCancellation)


class AppointmentCancellationAdmin(admin.ModelAdmin):
  readonly_fields = ('cancellation_time',)

admin.site.register(AvailableArea)
admin.site.register(User)
admin.site.register(Address)
admin.site.register(Device)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(TextMessage)
admin.site.register(Therapist)
admin.site.register(Patient)
admin.site.register(AwayPeriod)
admin.site.register(Bank)
admin.site.register(Card)
admin.site.register(Payment)
admin.site.register(PaymentProfile)
admin.site.register(Price)
admin.site.register(Certification)
admin.site.register(CertificationImage)
admin.site.register(Injury)
admin.site.register(InjuryImage)
admin.site.register(Appointment)
admin.site.register(AppointmentCancellation, AppointmentCancellationAdmin)
admin.site.register(AppointmentRequest)
admin.site.register(AppointmentRequestMessage)
admin.site.register(Review)
