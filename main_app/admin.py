from django.contrib import admin
from .models import Event, Comment, Photo, Rating

# Register your models here.
admin.site.register(Event)
admin.site.register(Comment)
admin.site.register(Photo)
admin.site.register(Rating)
