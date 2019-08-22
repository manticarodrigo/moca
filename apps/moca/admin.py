from django.contrib import admin
from .models import Conversation, Message, Participant, User, Address

admin.site.register(User)
admin.site.register(Address)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(Participant)
