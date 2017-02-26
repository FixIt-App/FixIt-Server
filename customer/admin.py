from django.contrib import admin

# Register your models here.
from customer.models import Customer

class CustomerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Customer, CustomerAdmin)
