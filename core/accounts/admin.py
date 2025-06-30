# tam61/accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Profile
from django.utils.html import format_html


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "phone",
        "full_name",
        "role",
        "is_active",
        "is_staff",
        "date_joined",
        "is_verified",
    )
    
    list_filter = (
        "role",
        "is_active",
        "is_staff",
    )
    
    search_fields = (
        "phone",
        "email",
        "full_name",
    )
    
    ordering = ("-date_joined",)
    
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        (_("👤 اطلاعات شخصی"), {"fields": ("full_name", "email", "role")}),
        (_("🔑 دسترسی‌ها و مجوزها"), {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
                "is_verified",
            )
        }),
        (_("⏱️ اطلاعات زمانی"), {"fields": ("date_joined",)}),
    )
    
    readonly_fields = ("date_joined",)
    
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone", "full_name", "email", "role", "password1", "password2"),
        }),
    )
    
    add_form_template = "admin/auth/user/add_form.html"
    change_user_password_template = None
    
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["full_name"]

admin.site.site_header = "💼 مدیریت کاربران"
admin.site.site_title = "💻 مدیریت کاربران"
admin.site.index_title = "🎯 داشبورد مدیریت"
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "first_name",
        "last_name",
        "national_id",
        "birth_date",
        "updated_date",
        "profile_picture_tag",
    )
    list_filter = ("birth_date",)
    search_fields = ("first_name", "last_name", "national_id", "user__phone")
    ordering = ("-updated_date",)

    fieldsets = (
        (None, {
            "fields": ("user",),
            "description": "👤 اطلاعات کاربر مربوط به این پروفایل"
        }),
        (_("🪪 اطلاعات هویتی"), {
            "fields": ("first_name", "last_name", "national_id", "birth_date"),
            "description": "📆 اطلاعات شناسنامه‌ای و تولد"
        }),
        (_("🏠 آدرس و 🖼️ تصویر پروفایل"), {
            "fields": ("address", "profile_picture", "profile_picture_tag"),
            "description": "📍 آدرس و نمایش تصویر کاربر"
        }),
        (_("⚙️ اطلاعات سیستمی"), {
            "fields": ("updated_date",),
            "description": "⏱️ تاریخ آخرین بروزرسانی"
        }),
    )

    readonly_fields = ("updated_date", "profile_picture_tag")

    def profile_picture_tag(self, obj):
        if obj.profile_picture:
            return format_html(
                '<div style="padding:4px; border:1px solid #ccc; display:inline-block;">'
                '<img src="{}" width="100" style="border-radius:12px; box-shadow:0 2px 5px rgba(0,0,0,0.1);" />'
                '</div>', obj.profile_picture.url
            )
        return format_html('<span style="color: #888;">❌ بدون عکس</span>')

    profile_picture_tag.short_description = "🖼️ پیش‌نمایش عکس"