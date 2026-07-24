from django.urls import path
from . import views

urlpatterns = [

    # ==========================================
    # Account CRUD
    # ==========================================

    path(
        '',
        views.account_list,
        name='accounts'
    ),

    path(
        'add/',
        views.add_account,
        name='add_account'
    ),

    path(
        'edit/<int:id>/',
        views.edit_account,
        name='edit_account'
    ),

    path(
        'delete/<int:id>/',
        views.delete_account,
        name='delete_account'
    ),

    # ==========================================
    # Export
    # ==========================================

    path(
        'export/csv/',
        views.export_accounts_csv,
        name='export_accounts_csv'
    ),

    path(
        'export/excel/',
        views.export_accounts_excel,
        name='export_accounts_excel'
    ),

    path(
        'export/pdf/',
        views.export_accounts_pdf,
        name='export_accounts_pdf'
    ),

    # ==========================================
    # Reports
    # ==========================================

    path(
        'report/',
        views.account_report,
        name='account_report'
    ),

]