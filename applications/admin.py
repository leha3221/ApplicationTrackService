from django.contrib import admin

from .models import Category, Request, Status

admin.site.site_header = "Кадровый сервис — администрирование"
admin.site.site_title = "Кадровый сервис"
admin.site.index_title = "Управление кадровыми данными"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("name",)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("name",)


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ("id", "employee", "category", "status", "date")
    list_filter = ("category", "status", "date")
    search_fields = ("employee__fio", "category__name", "status__name")
    list_select_related = ("employee", "category", "status")
    date_hierarchy = "date"
    ordering = ("-date", "-id")
    list_per_page = 25
