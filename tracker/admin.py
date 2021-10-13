from django.contrib import admin

from .models import Progress, Todo

admin.site.register(Todo)
admin.site.register(Progress)
