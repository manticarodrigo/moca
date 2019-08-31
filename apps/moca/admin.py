from django.contrib import admin

from .models import (Address, AttachmentMessage, Conversation, RequestMessage,
                     ResponseMessage, TextMessage, User)

admin.site.register(User)
admin.site.register(Address)
admin.site.register(Conversation)
admin.site.register(TextMessage)
admin.site.register(RequestMessage)
admin.site.register(ResponseMessage)
admin.site.register(AttachmentMessage)
