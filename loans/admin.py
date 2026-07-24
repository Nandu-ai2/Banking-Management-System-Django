from django.contrib import admin
from .models import Loan


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):

    list_display = (
        'loan_number',
        'customer',
        'account',
        'loan_type',
        'loan_amount',
        'interest_rate',
        'duration',
        'emi',
        'status',
        'start_date',
        'end_date',
    )

    search_fields = (
        'loan_number',
        'customer__customer_id',
        'customer__first_name',
        'customer__last_name',
        'account__account_number',
    )

    list_filter = (
        'loan_type',
        'status',
        'start_date',
    )

    ordering = (
        '-created_at',
    )

    list_per_page = 20