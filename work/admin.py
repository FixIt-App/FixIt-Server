from django.contrib import admin

from work.models import Work

class WorkAdmin(admin.ModelAdmin):
    list_display = ('id', 'state', 'get_customer', 'get_work', 'description', 'time', 'get_address')


    # this methods need to be defined because this fields are relationships
    def get_customer(self, obj):
        return obj.customer.user.username
    get_customer.admin_order_field = 'customer'
    get_customer.short_description = "Customer"

    def get_work(self, obj):
        return obj.worktype.name
    get_work.admin_order_field = 'worktype'
    get_work.short_description = 'Work Type'


    def get_address(self, obj):
        return obj.address.address
    get_address.admin_order_field = 'address'
    get_address.short_description = 'Address'

admin.site.register(Work, WorkAdmin)


