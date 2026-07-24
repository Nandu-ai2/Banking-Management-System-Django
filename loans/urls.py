from django.urls import path
from . import views

urlpatterns = [

    # ==========================
    # Loan List
    # ==========================
    path(
        "",
        views.loan_list,
        name="loans"
    ),

    # ==========================
    # Add Loan
    # ==========================
    path(
        "add/",
        views.add_loan,
        name="add_loan"
    ),

    # ==========================
    # Edit Loan
    # ==========================
    path(
        "edit/<int:id>/",
        views.edit_loan,
        name="edit_loan"
    ),

    # ==========================
    # Delete Loan
    # ==========================
    path(
        "delete/<int:id>/",
        views.delete_loan,
        name="delete_loan"
    ),

    # ==========================
    # Export CSV
    # ==========================
    path(
        "export/csv/",
        views.export_loans_csv,
        name="export_loans_csv"
    ),

    # ==========================
    # Export Excel
    # ==========================
    path(
        "export/excel/",
        views.export_loans_excel,
        name="export_loans_excel"
    ),

    # ==========================
    # Export PDF
    # ==========================
    path(
        "export/pdf/",
        views.export_loans_pdf,
        name="export_loans_pdf"
    ),

    # ==========================
    # Loan Report
    # ==========================
    path(
        "report/",
        views.loan_report,
        name="loan_report"
    ),
]