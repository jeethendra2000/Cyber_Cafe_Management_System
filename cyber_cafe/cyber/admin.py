from django.contrib import admin
from . models import Profile, Computer, Customer 

# Register your models here.

admin.site.register(Profile)
admin.site.register(Computer)

admin.site.register(Customer)