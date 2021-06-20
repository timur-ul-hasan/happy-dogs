from django.contrib import admin
from .models import (
    Dog,
    Visit
)

# Register your models here.

@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    pass

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    pass

