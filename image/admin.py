from django.contrib import admin

# Register your models here.
from image.models import Image

class ImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Image, ImageAdmin)