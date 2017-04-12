from django.contrib import admin
from worktype.models import WorkType, Category

class WorkTypeAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    
    class Meta:
        verbose_name = 'Category'
        verbose_plural_name = 'Categories'


admin.site.register(Category, CategoryAdmin)

admin.site.register(WorkType, WorkTypeAdmin)
