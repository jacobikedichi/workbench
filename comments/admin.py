from django.contrib import admin

from .models import ContentURL, Comment

admin.site.register(ContentURL)
admin.site.register(Comment)