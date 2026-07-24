from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        'customer_id',
        'first_name',
        'last_name',
        'phone',
        'email',
        'city',
        'status',
        'created_at',
    )

    search_fields = (
        'customer_id',
        'first_name',
        'last_name',
        'phone',
        'email',
        'city',
    )

    list_filter = (
        'status',
        'gender',
        'city',
    )

    ordering = (
        'customer_id',
    )