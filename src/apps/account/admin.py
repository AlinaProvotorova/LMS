from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import (
    DocumentsUser, Portfolio, StudentEducation, TeacherEducation, User
)


class UserAdmin(BaseUserAdmin):
    list_display = ["username", "email", "is_superuser"]
    list_filter = ["is_superuser", "roles"]

    fieldsets = [
        (None, {"fields": ['username', 'email', 'password']}),
        ("Персональная информация", {"fields": [
            "first_name", 'reporting', 'last_name',
            'date_of_birth', 'telephone', 'photo'
        ]}),
        ("Права доступа", {"fields": ["is_superuser", "roles"]}),
    ]

    filter_horizontal = ['roles']


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)


@admin.register(DocumentsUser)
class DocumentsUserAdmin(admin.ModelAdmin):
    list_display = ["title", "file", "user", "date_added", "id"]
    ordering = ["id"]
    list_filter = ["user"]
    list_per_page = 10


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ["title", "file", "user", "date_added", "id"]
    ordering = ["id"]
    list_filter = ["user"]
    list_per_page = 10


@admin.register(TeacherEducation)
class TeacherEducationAdmin(admin.ModelAdmin):
    list_display = ["teacher", "education"]
    list_filter = ["teacher", "education"]
    list_per_page = 10


@admin.register(StudentEducation)
class StudentEducationAdmin(admin.ModelAdmin):
    list_display = ["student", "education", "date"]
    list_filter = ["student", "education"]
    list_per_page = 10
