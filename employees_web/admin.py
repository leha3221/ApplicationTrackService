from django.contrib import admin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("fio", "department", "age")
    list_filter = ("department",)
    search_fields = ("fio", "department")
