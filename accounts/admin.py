from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):

    list_display = (
        'account_number',
        'customer',
        'account_type',
        'balance',
        'phone',
        'status',
        'created_at',
    )

    search_fields = (
        'account_number',
        'customer__customer_id',
        'customer__first_name',
        'customer__last_name',
        'phone',
        'email',
    )

    list_filter = (
        'account_type',
        'status',
    )

    ordering = (
        '-created_at',
    )