from django.contrib import admin

from .models import (Address, Conversation, Message, TextMessage, Patient, Therapist,
                     User, Device, PaymentProfile, Payment, Card, Bank,
                     PaymentProfile, Review, Appointment)

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
admin.site.register(Review)