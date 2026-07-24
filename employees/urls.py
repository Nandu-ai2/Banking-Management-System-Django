from django.urls import path

from . import views

urlpatterns = [
    # ==========================================
    # Employee List
    # ==========================================
    path(
        "",
        views.employee_list,
        name="employees"
    ),

    # ==========================================
    # Add Employee
    # ==========================================
    path(
        "add/",
        views.add_employee,
        name="add_employee"
    ),

    # ==========================================
    # Edit Employee
    # ==========================================
    path(
        "edit/<int:id>/",
        views.edit_employee,
        name="edit_employee"
    ),

    # ==========================================
    # Delete Employee
    # ==========================================
    path(
        "delete/<int:id>/",
        views.delete_employee,
        name="delete_employee"
    ),

    # ==========================================
    # Export CSV
    # ==========================================
    path(
        "export/csv/",
        views.export_employees_csv,
        name="export_employees_csv"
    ),

    # ==========================================
    # Export Excel
    # ==========================================
    path(
        "export/excel/",
        views.export_employees_excel,
        name="export_employees_excel"
    ),

    # ==========================================
    # Export PDF
    # ==========================================
    path(
        "export/pdf/",
        views.export_employees_pdf,
        name="export_employees_pdf"
    ),

    # ==========================================
    # Employee Report
    # ==========================================
    path(
        "report/",
        views.employee_report,
        name="employee_report"
    ),
]