from django.contrib import admin

# Register your models here.
from .models import City, Terminal


class TerminalInline(admin.TabularInline):
    model = Terminal
    extra = 1
    fields = ('name', 'address', 'phone', 'is_active', 'created_at')
    readonly_fields = ('created_at',)
    show_change_link = True


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'is_active', 'created_at')
    list_filter = ('is_active', 'province')
    search_fields = ('name', 'province')
    readonly_fields = ('created_at',)
    ordering = ('name',)

    fieldsets = (
        (None, {
            'fields': ('name', 'province', 'is_active')
        }),
        ('اطلاعات زمان', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    inlines = [TerminalInline]


@admin.register(Terminal)
class TerminalAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'phone', 'is_active', 'created_at')
    list_filter = ('is_active', 'city__province')
    search_fields = ('name', 'city__name', 'phone')
    readonly_fields = ('created_at',)
    ordering = ('city__name', 'name')

    fieldsets = (
        (None, {
            'fields': ('city', 'name', 'address', 'phone', 'is_active')
        }),
        ('اطلاعات زمان', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
