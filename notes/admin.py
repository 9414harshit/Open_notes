from django.contrib import admin
from .models import notes,group,Comment

admin.site.register(notes)
admin.site.register(group)
admin.site.register(Comment)