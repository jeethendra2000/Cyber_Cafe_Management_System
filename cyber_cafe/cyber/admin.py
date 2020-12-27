from django.contrib import admin
from . models import Profile, Computer, Customer, Price

# Register your models here.

# ~~~~~~ Another method of Defining ~~~~~
@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('price',)


admin.site.register(Profile)
admin.site.register(Computer)
admin.site.register(Customer)