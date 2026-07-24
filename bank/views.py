from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
import json

from accounts.models import Account
from customers.models import Customer
from transactions.models import Transaction
from loans.models import Loan
from employees.models import Employee


@login_required
def index(request):

    # =====================================================
    # Dashboard Statistics
    # =====================================================

    account_count = Account.objects.count()
    customer_count = Customer.objects.count()
    transaction_count = Transaction.objects.count()
    loan_count = Loan.objects.count()
    employee_count = Employee.objects.count()

    total_balance = (
        Account.objects.aggregate(
            total=Sum("balance")
        )["total"] or 0
    )

    # =====================================================
    # Recent Transactions
    # =====================================================

    recent_transactions = (
        Transaction.objects
        .select_related("account", "account__customer")
        .order_by("-transaction_date")[:5]
    )

    # =====================================================
    # Recent Customers
    # =====================================================

    recent_customers = (
        Customer.objects
        .order_by("-created_at")[:5]
    )

    # =====================================================
    # Monthly Transactions
    # =====================================================

    monthly_queryset = (
        Transaction.objects
        .annotate(
            month=TruncMonth("transaction_date")
        )
        .values("month")
        .annotate(
            total=Count("id")
        )
        .order_by("month")
    )

    monthly_labels = [
        item["month"].strftime("%b %Y")
        for item in monthly_queryset
    ]

    monthly_values = [
        item["total"]
        for item in monthly_queryset
    ]

    # =====================================================
    # Account Type
    # =====================================================

    account_queryset = (
        Account.objects
        .values("account_type")
        .annotate(
            total=Count("id")
        )
        .order_by("account_type")
    )

    account_labels = [
        item["account_type"]
        for item in account_queryset
    ]

    account_values = [
        item["total"]
        for item in account_queryset
    ]

    # =====================================================
    # Employee Departments
    # =====================================================

    department_queryset = (
        Employee.objects
        .values("department")
        .annotate(
            total=Count("id")
        )
        .order_by("department")
    )

    department_labels = [
        item["department"]
        for item in department_queryset
    ]

    department_values = [
        item["total"]
        for item in department_queryset
    ]

    # =====================================================
    # Loan Status
    # =====================================================

    loan_queryset = (
        Loan.objects
        .values("status")
        .annotate(
            total=Count("id")
        )
        .order_by("status")
    )

    loan_labels = [
        item["status"]
        for item in loan_queryset
    ]

    loan_values = [
        item["total"]
        for item in loan_queryset
    ]
    print("Monthly:", monthly_labels)
    print("Monthly Values:", monthly_values)

    print("Account:", account_labels)
    print("Account Values:", account_values)

    print("Department:", department_labels)
    print("Department Values:", department_values)

    print("Loan:", loan_labels)
    print("Loan Values:", loan_values)

    # =====================================================
    # Context
    # =====================================================

    context = {

        # Dashboard Cards

        "account_count": account_count,
        "customer_count": customer_count,
        "transaction_count": transaction_count,
        "loan_count": loan_count,
        "employee_count": employee_count,
        "total_balance": total_balance,

        # Tables

        "recent_transactions": recent_transactions,
        "recent_customers": recent_customers,

        # Monthly Chart

        "monthly_labels": json.dumps(monthly_labels),
        "monthly_values": json.dumps(monthly_values),

        # Account Chart

        "account_labels": json.dumps(account_labels),
        "account_values": json.dumps(account_values),

        # Department Chart

        "department_labels": json.dumps(department_labels),
        "department_values": json.dumps(department_values),

        # Loan Chart

        "loan_labels": json.dumps(loan_labels),
        "loan_values": json.dumps(loan_values),

    }

    return render(request, "index.html", context)