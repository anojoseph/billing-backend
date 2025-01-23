from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Role, Customer

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'role', 'is_active']
    list_filter = ['role', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['mobile_number', 'created_at', 'updated_at']
    search_fields = ['mobile_number']
    readonly_fields = ['created_at', 'updated_at']


# # auth_app/admin.py

# from django.contrib import admin
# from .models import CustomUser, Role

# class RoleAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')
#     search_fields = ('name',)

# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'phone_number', 'role', 'is_staff', 'is_active')
#     search_fields = ('username', 'phone_number')
#     list_filter = ('role', 'is_staff', 'is_active')
#     ordering = ('username',)

#     # Optionally customize the form to show only certain fields
#     fieldsets = (
#         (None, {
#             'fields': ('username', 'phone_number', 'password', 'role', 'is_staff', 'is_active')
#         }),
#     )

# # Register your models
# admin.site.register(Role, RoleAdmin)
# admin.site.register(CustomUser, CustomUserAdmin)
