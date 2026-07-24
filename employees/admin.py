from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        'employee_id',
        'first_name',
        'last_name',
        'department',
        'designation',
        'salary',
        'phone',
        'email',
        'status',
        'joining_date',
    )

    search_fields = (
        'employee_id',
        'first_name',
        'last_name',
        'designation',
        'phone',
        'email',
    )

    list_filter = (
        'department',
        'gender',
        'status',
        'joining_date',
    )

    ordering = (
        '-created_at',
    )

    list_per_page = 20