from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = (
        'account',
        'transaction_type',
        'amount',
        'transaction_date',
    )

    search_fields = (
        'account__account_number',
        'account__customer__first_name',
        'account__customer__last_name',
    )

    list_filter = (
        'transaction_type',
        'transaction_date',
    )

    ordering = (
        '-transaction_date',
    )