from django.contrib import admin
from worktype.models import WorkType

class WorkTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(WorkType, WorkTypeAdmin)
