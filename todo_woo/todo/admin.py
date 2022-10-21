from django.contrib import admin
from .models import Todo

class Admin_todo(admin.ModelAdmin):
    readonly_fields = ('created_at',)

admin.site.register(Todo, Admin_todo)
