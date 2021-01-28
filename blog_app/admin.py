from django.contrib import admin
from .models import Topic, Entry, Comment, Like
# Register your models here.
admin.site.register(Topic)
admin.site.register(Entry)
admin.site.register(Comment)
admin.site.register(Like)
