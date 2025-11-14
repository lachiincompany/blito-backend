from django.contrib import admin
from .models import BusCompany, BusCompanyRating
from django.utils.html import format_html
# Register your models here.

class BusCompanyRatingInline(admin.TabularInline):
    model = BusCompanyRating
    extra = 0
    readonly_fields = ['user', 'rating', 'created_at']
    can_delete = False

@admin.register(BusCompany)
class BusCompanyAdmin(admin.ModelAdmin):


    list_display = [
        'name', 
        'phone',
        'email_display',
        'address',
        'average_rating',
        'rating_count',
        'active_buses_count_display',
    ]

    list_filter = [
        'name',
    ]


    inlines = [BusCompanyRatingInline]

    readonly_fields = ['average_rating', 'rating_count', 'active_buses_count_display']

    search_fields = [
        'name',
        'email',
        'address',
        'phone',
    ]

    ordering = ['name']

    # list_per_page = 20

    fields = [
        'name',
        'email',
        'phone',
        'address',
        'active_buses_count_display',

    ]

    def email_display(self, obj):
        """Display email with mailto link"""
        if obj.email:
            return format_html(
                '<a href="mailto:{}" style="color: #0066cc;">{}</a>',
                obj.email,
                obj.email
            )
        return '-'
    email_display.short_description = 'ایمیل'


    def active_buses_count_display(self, obj):
        count = obj.active_buses_count
        return format_html('<span style="color: green; font-weight: bold;">{} فعال</span>', count)
    active_buses_count_display.short_description = 'تعداد اتوبوس‌های فعال'

    
    def average_rating_display(self, obj):
        rating = obj.average_rating()
        return f"{rating:.1f} ⭐" if rating else "بدون امتیاز"
    average_rating_display.short_description = 'میانگین امتیاز'

    def rating_count_display(self, obj):
        return obj.rating_count()
    rating_count_display.short_description = 'تعداد امتیاز'

    def average_rating_readonly(self, obj):
        return self.average_rating_display(obj)
    average_rating_readonly.short_description = 'میانگین امتیاز (خواندنی)'

    def rating_count_readonly(self, obj):
        return obj.rating_count()
    rating_count_readonly.short_description = 'تعداد امتیاز (خواندنی)'


admin.site.site_header = 'بلیتو - پنل مدیریت'
admin.site.site_title = 'بلیتو'
admin.site.index_title = 'مدیریت شرکت های اتوبوسرانی'


@admin.register(BusCompanyRating)
class BusCompanyRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'rating', 'created_at']
    list_filter = ['company', 'rating']
    search_fields = ['user__username', 'company__name']
    ordering = ['-created_at']