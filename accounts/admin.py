from django.contrib import admin
from accounts.models import CustomUser, Profile
from django.contrib.auth.admin import UserAdmin

# Register your models here.
# admin.site.register(CustomUser)
admin.site.register(Profile)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    search_fields = ['username', 'first_name', 'last_name',]
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser',)
    filter_horizontal = ('groups', 'user_permissions')
    fieldsets = (
        ('Usuario', {'fields': ('username', 'password')}),
        ('Personal Informations', {'fields': (
            'first_name',
            'last_name',
            'email',
        )}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions'
        )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

# admin.site.register(User, UserAdmin)