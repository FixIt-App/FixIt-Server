from django.contrib import admin

from work.models import Work

class WorkAdmin(admin.ModelAdmin):
    pass

admin.site.register(Work, WorkAdmin)


