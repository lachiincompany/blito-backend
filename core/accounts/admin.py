# tam61/accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Profile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "phone",
        "full_name",
        "role",
        "is_active",
        "is_staff",
        "date_joiend",
    )
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("phone", "email", "full_name")
    ordering = ("-date_joiend",)

    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        (_("اطلاعات شخصی"), {"fields": ("full_name", "email", "role")}),
        (
            _("دسترسی‌ها و مجوزها"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("اطلاعات زمانی"), {"fields": ("date_joiend",)}),
    )
    readonly_fields = ("date_joiend",)

    # فیلدهایی که در فرم ایجاد (ADD) کاربر جدید لازم هستند
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone", "full_name", "email", "role", "password1", "password2"),
            },
        ),
    )

    add_form_template = "admin/auth/user/add_form.html"
    change_user_password_template = None

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["full_name"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "first_name",
        "last_name",
        "national_id",
        "birth_date",
        "updated_date",
    )
    list_filter = ("birth_date",)
    search_fields = ("first_name", "last_name", "national_id", "user__phone")
    ordering = ("-updated_date",)

    fieldsets = (
        (None, {"fields": ("user",)}),
        (_("اطلاعات هویتی"), {"fields": ("first_name", "last_name", "national_id", "birth_date")}),
        (_("آدرس و تصویر"), {"fields": ("address", "profile_picture")}),
        (_("سیستم"), {"fields": ("updated_date",)}),
    )
    readonly_fields = ("updated_date",)
