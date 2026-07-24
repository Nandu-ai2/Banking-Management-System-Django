from django.contrib.auth.decorators import login_required
from decimal import Decimal

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Sum
from django.core.paginator import Paginator
from django.http import HttpResponse

import csv

from openpyxl import Workbook
from reportlab.pdfgen import canvas

from .models import Transaction
from .forms import TransactionForm
from accounts.models import Account


# =====================================
# Common Transaction Query
# =====================================

def get_filtered_transactions(request):

    search = request.GET.get("search", "").strip()

    transaction_type = request.GET.get("transaction_type", "")

    sort = request.GET.get("sort", "-transaction_date")

    transactions = Transaction.objects.select_related(
        "account",
        "account__customer"
    )

    if search:

        transactions = transactions.filter(
            Q(account__account_number__icontains=search) |
            Q(account__customer__customer_id__icontains=search) |
            Q(account__customer__first_name__icontains=search) |
            Q(account__customer__last_name__icontains=search)
        )

    if transaction_type:

        transactions = transactions.filter(
            transaction_type=transaction_type
        )

    transactions = transactions.order_by(sort)

    return transactions


# =====================================
# Transaction List
# =====================================

@login_required
def transaction_list(request):

    search = request.GET.get("search", "").strip()

    transactions = get_filtered_transactions(request)

    paginator = Paginator(transactions, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "transactions/transactions.html",
        {
            "transactions": page_obj,
            "page_obj": page_obj,
            "search": search,
            "transaction_type": request.GET.get("transaction_type", ""),
            "sort": request.GET.get("sort", "-transaction_date"),
        }
    )


# ==========================
# Add Transaction
# ==========================

@login_required
def add_transaction(request):

    if request.method == "POST":

        form = TransactionForm(request.POST)

        if form.is_valid():

            transaction = form.save(commit=False)

            account = transaction.account

            amount = Decimal(transaction.amount)

            if transaction.transaction_type == "Deposit":

                account.balance += amount

            elif transaction.transaction_type == "Withdraw":

                if account.balance < amount:

                    messages.error(
                        request,
                        "Insufficient account balance."
                    )

                    return render(
                        request,
                        "transactions/add_transactions.html",
                        {
                            "form": form
                        }
                    )

                account.balance -= amount

            account.save()

            transaction.save()

            messages.success(
                request,
                "Transaction added successfully."
            )

            return redirect("transactions")

    else:

        form = TransactionForm()

    return render(
        request,
        "transactions/add_transactions.html",
        {
            "form": form
        }
    )


# ==========================
# Edit Transaction
# ==========================

@login_required
def edit_transaction(request, id):

    transaction = get_object_or_404(
        Transaction,
        id=id
    )

    old_account = transaction.account

    old_amount = Decimal(transaction.amount)

    old_type = transaction.transaction_type

    if request.method == "POST":

        form = TransactionForm(
            request.POST,
            instance=transaction
        )

        if form.is_valid():

            # Reverse old transaction

            if old_type == "Deposit":

                old_account.balance -= old_amount

            elif old_type == "Withdraw":

                old_account.balance += old_amount

            old_account.save()

            transaction = form.save(commit=False)

            account = transaction.account

            amount = Decimal(transaction.amount)

            if transaction.transaction_type == "Deposit":

                account.balance += amount

            elif transaction.transaction_type == "Withdraw":

                if account.balance < amount:

                    messages.error(
                        request,
                        "Insufficient account balance."
                    )

                    return render(
                        request,
                        "transactions/edit_transactions.html",
                        {
                            "form": form
                        }
                    )

                account.balance -= amount

            account.save()

            transaction.save()

            messages.success(
                request,
                "Transaction updated successfully."
            )

            return redirect("transactions")

    else:

        form = TransactionForm(
            instance=transaction
        )

    return render(
        request,
        "transactions/edit_transactions.html",
        {
            "form": form,
            "transaction": transaction
        }
    )
# ==========================
# Delete Transaction
# ==========================

@login_required
def delete_transaction(request, id):

    transaction = get_object_or_404(
        Transaction,
        id=id
    )

    if request.method == "POST":

        account = transaction.account

        amount = Decimal(transaction.amount)

        if transaction.transaction_type == "Deposit":

            account.balance -= amount

        elif transaction.transaction_type == "Withdraw":

            account.balance += amount

        account.save()

        transaction.delete()

        messages.success(
            request,
            "Transaction deleted successfully."
        )

        return redirect("transactions")

    return render(
        request,
        "transactions/delete_transactions.html",
        {
            "transaction": transaction
        }
    )


# =====================================
# Export Transactions - CSV
# =====================================

@login_required
def export_transactions_csv(request):

    transactions = get_filtered_transactions(request)

    response = HttpResponse(content_type="text/csv")

    response["Content-Disposition"] = (
        'attachment; filename="transactions.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        "Account Number",
        "Customer",
        "Transaction Type",
        "Amount",
        "Date"
    ])

    for transaction in transactions:

        writer.writerow([
            transaction.account.account_number,
            f"{transaction.account.customer.first_name} "
            f"{transaction.account.customer.last_name}",
            transaction.transaction_type,
            transaction.amount,
            transaction.transaction_date,
        ])

    return response


# =====================================
# Export Transactions - Excel
# =====================================

@login_required
def export_transactions_excel(request):

    transactions = get_filtered_transactions(request)

    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Transactions"

    sheet.append([
        "Account Number",
        "Customer",
        "Transaction Type",
        "Amount",
        "Date"
    ])

    for transaction in transactions:

        sheet.append([
            transaction.account.account_number,
            f"{transaction.account.customer.first_name} "
            f"{transaction.account.customer.last_name}",
            transaction.transaction_type,
            float(transaction.amount),
            str(transaction.transaction_date),
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = (
        'attachment; filename="transactions.xlsx"'
    )

    workbook.save(response)

    return response


# =====================================
# Export Transactions - PDF
# =====================================

@login_required
def export_transactions_pdf(request):

    transactions = get_filtered_transactions(request)

    response = HttpResponse(content_type="application/pdf")

    response["Content-Disposition"] = (
        'attachment; filename="transactions.pdf"'
    )

    pdf = canvas.Canvas(response)

    y = 800

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(180, y, "Transaction Report")

    y -= 30

    pdf.setFont("Helvetica", 10)

    for transaction in transactions:

        pdf.drawString(
            30,
            y,
            f"{transaction.account.account_number} | "
            f"{transaction.account.customer.first_name} "
            f"{transaction.account.customer.last_name} | "
            f"{transaction.transaction_type} | "
            f"₹ {transaction.amount}"
        )

        y -= 20

        if y < 50:

            pdf.showPage()

            pdf.setFont("Helvetica", 10)

            y = 800

    pdf.save()

    return response


# =====================================
# Transaction Report
# =====================================

@login_required
def transaction_report(request):

    start_date = request.GET.get("start_date")

    end_date = request.GET.get("end_date")

    transactions = Transaction.objects.select_related(
        "account",
        "account__customer"
    )

    if start_date and end_date:

        transactions = transactions.filter(
            transaction_date__date__range=[
                start_date,
                end_date
            ]
        )

    total_transactions = transactions.count()

    total_amount = transactions.aggregate(
        total=Sum("amount")
    )["total"] or 0

    return render(
        request,
        "transactions/transaction_report.html",
        {
            "transactions": transactions,
            "start_date": start_date,
            "end_date": end_date,
            "total_transactions": total_transactions,
            "total_amount": total_amount,
        }
    )