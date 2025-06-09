from django.contrib import admin
from .models import Seat
from django.utils.html import format_html

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = (
        "trip",
        "seat_number",
        "status_icon",
        "reserved_by_display",
        "reserved_at",
    )
    list_filter = ("is_reserved", "trip__departure_datetime")
    search_fields = ("seat_number", "reserved_by__user__phone", "reserved_by__user__username")
    ordering = ["trip", "seat_number"]
    readonly_fields = ("reserved_at",)

    fieldsets = (
        ("🪑 اطلاعات صندلی", {
            "fields": ("trip", "seat_number", "is_reserved")
        }),
        ("👤 اطلاعات رزرو", {
            "fields": ("reserved_by", "reserved_at")
        }),
    )

    def status_icon(self, obj):
        if obj.is_reserved:
            return format_html("<span style='color:red;'>✅ رزرو شده</span>")
        return format_html("<span style='color:green;'>🟢 آزاد</span>")
    status_icon.short_description = "وضعیت"

    def reserved_by_display(self, obj):
        if obj.reserved_by:
            return f"{obj.reserved_by.first_name} {obj.reserved_by.last_name}"
        return "-"
    reserved_by_display.short_description = "رزرو توسط"
