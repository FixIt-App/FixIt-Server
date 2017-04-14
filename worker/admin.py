from django.contrib import admin
from worker.models import Worker

class WorkerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Worker, WorkerAdmin)
