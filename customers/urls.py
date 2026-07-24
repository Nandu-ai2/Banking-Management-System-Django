from django.urls import path
from . import views

urlpatterns = [

    # ==========================================
    # Customer CRUD
    # ==========================================

    path(
        '',
        views.customer_list,
        name='customers'
    ),

    path(
        'add/',
        views.add_customer,
        name='add_customer'
    ),

    path(
        'edit/<int:id>/',
        views.edit_customer,
        name='edit_customer'
    ),

    path(
        'delete/<int:id>/',
        views.delete_customer,
        name='delete_customer'
    ),

    # ==========================================
    # Export
    # ==========================================

    path(
        'export/csv/',
        views.export_customers_csv,
        name='export_customers_csv'
    ),

    path(
        'export/excel/',
        views.export_customers_excel,
        name='export_customers_excel'
    ),

    path(
        'export/pdf/',
        views.export_customers_pdf,
        name='export_customers_pdf'
    ),

    # ==========================================
    # Report
    # ==========================================

    path(
        'report/',
        views.customer_report,
        name='customer_report'
    ),

]