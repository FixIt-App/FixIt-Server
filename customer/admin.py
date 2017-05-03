from django.contrib import admin

# Register your models here.
from customer.models import Customer, Address, Confirmation

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_username')

    def get_username(self, obj):
        return obj.user.username
    get_username.admin_order_field = 'username'
    get_username.short_description = "username"

admin.site.register(Customer, CustomerAdmin)

class AddressAdmin(admin.ModelAdmin):
    pass

admin.site.register(Address, AddressAdmin)


class ConfirmationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Confirmation, ConfirmationAdmin)
