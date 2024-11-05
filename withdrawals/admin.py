from django.contrib import admin
from .models import WithdrawalRequest

class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('user__username',)

admin.site.register(WithdrawalRequest, WithdrawalRequestAdmin)