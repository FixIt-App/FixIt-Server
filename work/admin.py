from django.contrib import admin

from work.models import Work, DynamicPricing, Rating, Transaction, TransactionItem

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

class DynamicPricingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start', 'end', 'multiplier')

class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'score', 'work')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'receipt_number', 'value')

class TransactionItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_type', 'price', 'description', 'get_trx')

    def get_trx(self, obj):
        return obj.trx.receipt_number
    get_trx.admin_order_field = 'Receipt Number'
    get_trx.short_description = "receipt number"

admin.site.register(Work, WorkAdmin)
admin.site.register(DynamicPricing, DynamicPricingAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(TransactionItem, TransactionItemAdmin)


