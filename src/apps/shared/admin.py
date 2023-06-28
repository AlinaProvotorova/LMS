from django.contrib import admin

from .models import DocumentsUniversity


@admin.register(DocumentsUniversity)
class DocumentsUniversityAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "document_name", "path", "date_added"]
    list_editable = ["title", "document_name", "path"]
