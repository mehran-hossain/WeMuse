from django.contrib import admin

# Register your models here.
from .models import Audio, Sample

admin.site.register(Audio)
admin.site.register(Sample)