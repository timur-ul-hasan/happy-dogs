from django.contrib import admin
from .models import (
    Dog
)

# Register your models here.

@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    pass
