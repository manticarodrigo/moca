from django.contrib import admin

from .models import (User, Therapist, Patient, AvailableArea, Address, Device, MerchantProfile,
                     PaymentProfile, Payment, Card, Bank, Conversation, Message, CompositeMessage,
                     CompositeMessageImage, AppointmentRequestMessage, Price, Note, NoteImage,
                     Review, Appointment, AppointmentRequest, AppointmentCancellation, Issue,
                     AwayPeriod, Certification, CertificationImage, Injury, InjuryImage)


class AppointmentCancellationAdmin(admin.ModelAdmin):
  readonly_fields = ('cancellation_time', )


admin.site.register(User)
admin.site.register(Therapist)
admin.site.register(Patient)
admin.site.register(AvailableArea)
admin.site.register(Address)
admin.site.register(Device)
admin.site.register(MerchantProfile)
admin.site.register(PaymentProfile)
admin.site.register(Payment)
admin.site.register(Bank)
admin.site.register(Card)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(CompositeMessage)
admin.site.register(CompositeMessageImage)
admin.site.register(AppointmentRequestMessage)
admin.site.register(Price)
admin.site.register(Note)
admin.site.register(NoteImage)
admin.site.register(Review)
admin.site.register(Appointment)
admin.site.register(AppointmentRequest)
admin.site.register(AppointmentCancellation, AppointmentCancellationAdmin)
admin.site.register(Issue)
admin.site.register(AwayPeriod)
admin.site.register(Certification)
admin.site.register(CertificationImage)
admin.site.register(Injury)
admin.site.register(InjuryImage)
