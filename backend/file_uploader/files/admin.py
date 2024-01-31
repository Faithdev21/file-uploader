from typing import Tuple

from django.contrib import admin

from files.models import File


@admin.register(File)
class FilesAdmin(admin.ModelAdmin):
    list_display: Tuple = ('id', 'file', 'uploaded_at', 'processed',)
