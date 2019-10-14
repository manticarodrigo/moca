from django.contrib import admin

from .models import (Address, MediaMessage, Conversation, Patient, AppointmentMessage, Therapist,
                     User, Device, PaymentProfile,  Payment, Card, Bank)

admin.site.register(User)
admin.site.register(Address)
admin.site.register(Conversation)
admin.site.register(MediaMessage)
admin.site.register(AppointmentMessage)
admin.site.register(Therapist)
admin.site.register(Patient)
admin.site.register(Device)
admin.site.register(Bank)
admin.site.register(Card)
admin.site.register(Payment)
admin.site.register(PaymentProfile)