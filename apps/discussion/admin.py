from django.contrib import admin
from .models import DiscussionEntry, DiscussionTopic



admin.site.register(DiscussionTopic)
admin.site.register(DiscussionEntry)

# Register your models here.
