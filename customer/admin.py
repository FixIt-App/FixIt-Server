from django.contrib import admin

# Register your models here.
from customer.models import Customer, Address, Confirmation

class CustomerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Customer, CustomerAdmin)

class AddressAdmin(admin.ModelAdmin):
    pass

admin.site.register(Address, AddressAdmin)


class ConfirmationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Confirmation, ConfirmationAdmin)
