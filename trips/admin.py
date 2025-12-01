from django.contrib import admin
from .models import Trip
from django.utils.html import format_html
from django.utils.timezone import localtime

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = (
        "colored_status",
        "route",
        "bus",
        "short_departure",
        "short_arrival",
        "current_price",
        # "driver_phone",
    )
    list_filter = ("status", "route__company", "departure_datetime")
    search_fields = ("route__origin__city__name", "route__destination__city__name")
    ordering = ["-departure_datetime"]
    readonly_fields = ("created_at",)

    fieldsets = (
        ("🚌 اطلاعات کلی سفر", {
            "fields": ("route", "bus", "status"),
        }),
        ("⏰ زمان‌بندی", {
            "fields": ("departure_datetime", "arrival_datetime"),
        }),
        ("💰 قیمت", {
            "fields": ("current_price",),
        }),
        ("📅 اطلاعات سیستمی", {
            "fields": ("created_at",),
        }),
    )
    

    def colored_status(self, obj):
        emojis = {
            "SCHEDULED": "🗓️ برنامه‌ریزی",
            "BOARDING": "🧍‍♂️ در حال سوار شدن",
            "DEPARTED": "🚍 حرکت کرده",
            "ARRIVED": "✅ رسیده",
            "CANCELLED": "❌ لغو شده",
        }
        return emojis.get(obj.status, "❓ نامشخص")
    colored_status.short_description = "وضعیت 🧭"

    def short_departure(self, obj):
        return localtime(obj.departure_datetime).strftime("🕒 %Y-%m-%d %H:%M")
    short_departure.short_description = "حرکت"

    def short_arrival(self, obj):
        return localtime(obj.arrival_datetime).strftime("🏁 %Y-%m-%d %H:%M")
    short_arrival.short_description = "رسیدن"
