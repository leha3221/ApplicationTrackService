from django.contrib import admin

from applications.models import Request

from .models import Employee


class RequestInline(admin.TabularInline):
    model = Request
    extra = 0
    fields = ("category", "status", "date")
    show_change_link = True


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "fio", "department", "age")
    list_filter = ("department",)
    search_fields = ("fio", "department")
    ordering = ("fio", "id")
    list_per_page = 25
    inlines = (RequestInline,)
