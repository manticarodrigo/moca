from django.contrib import admin

from .models import (Address, AttachmentMessage, Conversation, Patient, RequestMessage,
                     ResponseMessage, TextMessage, Therapist, User, Device)

admin.site.register(User)
admin.site.register(Address)
admin.site.register(Conversation)
admin.site.register(TextMessage)
admin.site.register(RequestMessage)
admin.site.register(ResponseMessage)
admin.site.register(AttachmentMessage)
admin.site.register(Therapist)
admin.site.register(Patient)
admin.site.register(Device)