from django.contrib import admin
from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'amount', 'gateway', 'status', 'authority', 'paid_at')
    list_filter = ('gateway', 'status', 'created_at')
    search_fields = ('authority', 'reference_id', 'reservation__reservation_code')
    readonly_fields = ('authority', 'created_at', 'updated_at', 'paid_at')
