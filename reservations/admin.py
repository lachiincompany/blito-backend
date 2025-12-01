from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "reservation_code",
        "user_display",
        "seat_number",
        "trip_route",
        "payment_status_colored",
        "total_price",
        "created_at",
    )
    list_filter = ("payment_status", "created_at")
    search_fields = ("reservation_code", "user__user__phone", "user__user__full_name")
    ordering = ["-created_at"]
    readonly_fields = ("created_at", "updated_at", "reservation_code", "total_price")

    fieldsets = (
        ("🧾 اطلاعات رزرو", {
            "fields": ("reservation_code", "user", "seat", "payment_status", "total_price")
        }),
        ("🕓 زمان", {
            "fields": ("created_at", "updated_at")
        }),
    )

    def user_display(self, obj):
        return obj.user.first_name
    user_display.short_description = "کاربر"

    def seat_number(self, obj):
        return f"صندلی {obj.seat.seat_number}"
    seat_number.short_description = "شماره صندلی"

    def trip_route(self, obj):
        trip = obj.seat.trip
        return f"{trip.route.origin.city.name} → {trip.route.destination.city.name}"
    trip_route.short_description = "مسیر سفر"

    def payment_status_colored(self, obj):
        color_map = {
            'PENDING': '🟡 در انتظار',
            'PAID': '🟢 پرداخت شده',
            'FAILED': '🔴 ناموفق',
            'REFUNDED': '🔵 برگشت داده شده',
        }
        return color_map.get(obj.payment_status, obj.payment_status)
    payment_status_colored.short_description = "وضعیت پرداخت"
