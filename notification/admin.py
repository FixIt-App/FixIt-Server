from django.contrib import admin
from .models import NotificationToken, Notification

class NotificationTokenAdmin(admin.ModelAdmin):
    list_diplay = ('id', 'token' , 'token_type', 'platform_type', 'get_user')

    def get_user(self, obj):
        return obj.user.username
    
    get_user.admin_order_field = 'user'
    get_user.short_description = 'User'

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id',)

admin.site.register(NotificationToken, NotificationTokenAdmin)
admin.site.register(Notification, NotificationAdmin)
