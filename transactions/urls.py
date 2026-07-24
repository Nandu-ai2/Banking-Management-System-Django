from django.urls import path
from . import views

urlpatterns = [

    # ==========================
    # Transaction List
    # ==========================
    path(
        "",
        views.transaction_list,
        name="transactions"
    ),

    # ==========================
    # Add Transaction
    # ==========================
    path(
        "add/",
        views.add_transaction,
        name="add_transaction"
    ),

    # ==========================
    # Edit Transaction
    # ==========================
    path(
        "edit/<int:id>/",
        views.edit_transaction,
        name="edit_transaction"
    ),

    # ==========================
    # Delete Transaction
    # ==========================
    path(
        "delete/<int:id>/",
        views.delete_transaction,
        name="delete_transaction"
    ),

    # ==========================
    # Export CSV
    # ==========================
    path(
        "export/csv/",
        views.export_transactions_csv,
        name="export_transactions_csv"
    ),

    # ==========================
    # Export Excel
    # ==========================
    path(
        "export/excel/",
        views.export_transactions_excel,
        name="export_transactions_excel"
    ),

    # ==========================
    # Export PDF
    # ==========================
    path(
        "export/pdf/",
        views.export_transactions_pdf,
        name="export_transactions_pdf"
    ),

    # ==========================
    # Transaction Report
    # ==========================
    path(
        "report/",
        views.transaction_report,
        name="transaction_report"
    ),

]