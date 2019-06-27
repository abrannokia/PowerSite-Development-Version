from django.contrib import admin
from .models import Person, Mail

# Register your models here.
admin.site.register(Person)
admin.site.register(Mail)