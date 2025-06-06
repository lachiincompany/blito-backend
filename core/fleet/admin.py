from django.contrib import admin
from .models import Fleet
from django.utils.html import format_html


@admin.register(Fleet)
class FleetAdmin(admin.ModelAdmin):
    list_display = (
        'bus_number', 'company', 'license_plate', 'driver',
        'bus_type', 'year', 'capacity', 'facilities_display', 'image_tag'
    )
    list_filter = (
        'company', 'bus_type', 'year', 'has_wifi', 'has_ac',
        'has_tv', 'has_charging', 'has_blanket', 'has_food_service'
    )
    search_fields = ('bus_number', 'license_plate', 'model', 'brand', 'driver__username', 'company__name')
    ordering = ('company', 'bus_number')
    readonly_fields = ('image_tag',)
    list_per_page = 25

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': (
                'company', 'driver', 'bus_number', 'license_plate',
                'model', 'brand', 'year', 'capacity', 'bus_type'
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

admin.site.site_header = 'مدیریت ناوگان اتوبوس'
admin.site.site_title = 'مدیریت ناوگان اتوبوس'
admin.site.index_title = 'پنل مدیریت ناوگان اتوبوس'