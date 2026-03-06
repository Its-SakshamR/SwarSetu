from django.contrib import admin
from .models import Song, LyricVersion, Annotation

admin.site.register(Song)
admin.site.register(LyricVersion)
admin.site.register(Annotation)