from django.contrib import admin
from django.utils.html import format_html
from .models import Fleet
from accounts.models import Profile

@admin.register(Fleet)
class FleetAdmin(admin.ModelAdmin):
    list_display = (
        'bus_number', 'company', 'license_plate', 'driver',
        'bus_type', 'year', 'capacity', 'facilities_display', 'image_tag', 'is_active'
    )
    list_filter = (
        'company', 'bus_type', 'year', 'has_wifi', 'has_ac',
        'has_tv', 'has_charging', 'has_blanket', 'has_food_service'
    )
    search_fields = (
        'bus_number', 'license_plate', 'model', 'brand',
        'driver__first_name', 'driver__last_name', 'company__name'
    )
    ordering = ('company', 'bus_number')
    readonly_fields = ('image_tag',)
    list_per_page = 25

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': (
                'company', 'driver', 'bus_number', 'license_plate',
                'model', 'brand', 'year', 'capacity', 'bus_type', 'is_active'
            )
        }),
        ('امکانات رفاهی', {
            'fields': (
                'has_wifi', 'has_ac', 'has_tv',
                'has_charging', 'has_blanket', 'has_food_service'
            )
        }),
        ('تصاویر', {
            'fields': ('image', 'interior_image', 'image_tag')
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "driver":
            kwargs["queryset"] = Profile.objects.filter(user__role="driver")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def facilities_display(self, obj):
        facilities = []
        if obj.has_wifi:
            facilities.append('📶')
        if obj.has_ac:
            facilities.append('❄️')
        if obj.has_tv:
            facilities.append('📺')
        if obj.has_charging:
            facilities.append('🔌')
        if obj.has_blanket:
            facilities.append('🛏️')
        if obj.has_food_service:
            facilities.append('🍱')
        return " ".join(facilities) if facilities else "ندارد"
    facilities_display.short_description = 'امکانات'

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" style="border-radius: 8px;" />', obj.image.url)
        return "تصویر ندارد"
    image_tag.short_description = 'پیش‌نمایش تصویر'
