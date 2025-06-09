from django.contrib import admin

# Register your models here.
from django import forms
from django.contrib import admin
from .models import Route




class RouteAdminForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = '__all__'

    estimated_duration = forms.DurationField(
        widget=forms.TextInput(attrs={'placeholder': 'مثلاً 2:30:00 برای ۲ ساعت و نیم'}),
        help_text='مدت زمان را به فرمت HH:MM:SS وارد کنید.' , 
        label= 'مدت زمان تقریبی سفر' ,
    )

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    form = RouteAdminForm
    list_display = (
        'colored_route', 'company', 'bus_type_display', 
        'base_price', 'distance_km', 'duration_pretty', 'is_active', 'created_at'
    )
    list_filter = ('is_active', 'bus_type', 'company', 'origin__city__name', 'destination__city__name')
    search_fields = (
        'origin__city__name', 'destination__city__name', 'company__name'
    )
    readonly_fields = ('created_at',)
    ordering = ('origin__city__name', 'destination__city__name', 'company__name')

    fieldsets = (
        (None, {
            'fields': ('origin', 'destination', 'company', 'bus_type', 'base_price', 'distance_km', 'estimated_duration', 'is_active')
        }),
        ('زمان ساخت', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    def colored_route(self, obj):
        return f"🌆 {obj.destination.city.name} ➡️ {obj.origin.city.name}"
    colored_route.short_description = "مسیر"

    def duration_pretty(self, obj):
        total_minutes = int(obj.estimated_duration.total_seconds() // 60)
        hours, minutes = divmod(total_minutes, 60)
        return f"⏱️ {hours} ساعت و {minutes} دقیقه"
    duration_pretty.short_description = "مدت زمان سفر"

    def bus_type_display(self, obj):
        icons = {
            'standard': '🚌 معمولی',
            'luxury': '🛻 لوکس',
            'vip': '🚍 وی‌آی‌پی'
        }
        return icons.get(obj.bus_type, obj.bus_type)
    bus_type_display.short_description = "نوع اتوبوس"
