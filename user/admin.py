from django.contrib import admin

from .models import CustomUser

admin.site.site_header = "Ogani Admin Panel"
admin.site.site_title = "Ogani Admin Panel"
admin.site.index_title = "Welcome to Ogani Admin Panel"
admin.site.empty_value_display = "Not available"

from django.contrib.auth.admin import UserAdmin

from django.contrib.auth.models import Group

# Register your models here.

class CustomUserAdmin(UserAdmin):
    """
    CustomUser Admin Interface
    """

    model = CustomUser
    ordering = ('phone_number',)
    date_hierarchy = 'date_joined'
    list_per_page = 5
    # list_editable = ('phone_number',)
    search_fields = ('phone_number',)
    list_display = (
        'id',
        'phone_number',
        'is_active',
        'is_staff',
        'is_superuser',
        'last_login',
        'date_joined',
    )
    filter_horizontal = (
        'groups',
        'user_permissions',
    )
    list_display_links = (
        'id',
        # 'phone_number',
    )
    readonly_fields = (
        'id',
        'last_login',
        'date_joined',
    )
    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
    )

    fieldsets = (
        ('Login', {
            'fields': ('phone_number', 'password',),
            'classes': ('wide',),
        }),
        ("Permissions", {
            'fields': ('is_superuser', 'is_staff', 'is_active',),
            'classes': ('wide',),
        }),
        ("Groups and Permissions", {
            'fields': ('groups', 'user_permissions',),
            'classes': ('wide',),
        }),
        ("Important Dates", {
            'fields': ('date_joined', 'last_login',),
            'classes': ('wide', 'collapse',),
        }),
        ("ID", {
            'fields': ('id',),
            'classes': ('wide', 'collapse',),
        }),
    )
    add_fieldsets = (
        ('Create Super User', {
            'fields': ('phone_number',),
            'classes': ('wide',),
        }),
        ('Passwords', {
            'fields': ('password1', 'password2',),
            'classes': ('wide',),
        }),
        ("Permissions", {
            'fields': ('is_superuser', 'is_staff',),
            'classes': ('wide',),
        }),
        ("Groups and Permissions", {
            'fields': ('groups', 'user_permissions',),
            'classes': ('wide',),
        }),
    )

# admin.site.unregister(Group) # Unregister the Group model if not needed


admin.site.register(CustomUser, CustomUserAdmin)
