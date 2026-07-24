import csv

from openpyxl import Workbook
from reportlab.pdfgen import canvas

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Sum
from django.core.paginator import Paginator

from .models import Account
from .forms import AccountForm


# ==========================================
# Common Filter Query
# ==========================================

def get_filtered_accounts(request):

    search = request.GET.get("search", "").strip()
    account_type = request.GET.get("account_type", "")
    status = request.GET.get("status", "")
    sort = request.GET.get("sort", "-id")

    accounts = Account.objects.select_related(
        "customer"
    )

    if search:

        accounts = accounts.filter(
            Q(account_number__icontains=search) |
            Q(customer__customer_id__icontains=search) |
            Q(customer__first_name__icontains=search) |
            Q(customer__last_name__icontains=search) |
            Q(account_type__icontains=search) |
            Q(phone__icontains=search) |
            Q(status__icontains=search)
        )

    if account_type:

        accounts = accounts.filter(
            account_type=account_type
        )

    if status:

        accounts = accounts.filter(
            status=status
        )

    accounts = accounts.order_by(sort)

    return accounts


# ==========================================
# Account List
# ==========================================

@login_required
def account_list(request):

    search = request.GET.get("search", "").strip()

    accounts = get_filtered_accounts(request)

    paginator = Paginator(accounts, 10)

    page_number = request.GET.get("page")

    accounts = paginator.get_page(page_number)

    return render(
        request,
        "accounts/accounts.html",
        {
            "accounts": accounts,
            "search": search,
            "account_type": request.GET.get("account_type", ""),
            "status": request.GET.get("status", ""),
            "sort": request.GET.get("sort", "-id"),
        }
    )


# ==========================================
# Add Account
# ==========================================

@login_required
def add_account(request):

    if request.method == "POST":

        form = AccountForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Account added successfully."
            )

            return redirect("accounts")

        else:

            print(form.errors)

    else:

        form = AccountForm()

    return render(
        request,
        "accounts/add_account.html",
        {
            "form": form
        }
    )


# ==========================================
# Edit Account
# ==========================================

@login_required
def edit_account(request, id):

    account = get_object_or_404(
        Account,
        id=id
    )

    if request.method == "POST":

        form = AccountForm(
            request.POST,
            instance=account
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Account updated successfully."
            )

            return redirect("accounts")

    else:

        form = AccountForm(
            instance=account
        )

    return render(
        request,
        "accounts/edit_account.html",
        {
            "form": form,
            "account": account
        }
    )


# ==========================================
# Delete Account
# ==========================================

@login_required
def delete_account(request, id):

    account = get_object_or_404(
        Account,
        id=id
    )

    if request.method == "POST":

        account.delete()

        messages.success(
            request,
            "Account deleted successfully."
        )

        return redirect("accounts")

    return render(
        request,
        "accounts/delete_account.html",
        {
            "account": account
        }
    )


# ==========================================
# Export CSV
# ==========================================

@login_required
def export_accounts_csv(request):

    accounts = get_filtered_accounts(request)

    response = HttpResponse(
        content_type="text/csv"
    )

    response["Content-Disposition"] = (
        'attachment; filename="accounts.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        "Account Number",
        "Customer ID",
        "Customer Name",
        "Account Type",
        "Phone",
        "Balance",
        "Status",
    ])

    for account in accounts:

        writer.writerow([
            account.account_number,
            account.customer.customer_id,
            f"{account.customer.first_name} {account.customer.last_name}",
            account.account_type,
            account.phone,
            account.balance,
            account.status,
        ])

    return response


# ==========================================
# Export Excel
# ==========================================

@login_required
def export_accounts_excel(request):

    accounts = get_filtered_accounts(request)

    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Accounts"

    sheet.append([
        "Account Number",
        "Customer ID",
        "Customer Name",
        "Account Type",
        "Phone",
        "Balance",
        "Status",
    ])

    for account in accounts:

        sheet.append([
            account.account_number,
            account.customer.customer_id,
            f"{account.customer.first_name} {account.customer.last_name}",
            account.account_type,
            account.phone,
            float(account.balance),
            account.status,
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = (
        'attachment; filename="accounts.xlsx"'
    )

    workbook.save(response)

    return response


# ==========================================
# Export PDF
# ==========================================

@login_required
def export_accounts_pdf(request):

    accounts = get_filtered_accounts(request)

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        'attachment; filename="accounts.pdf"'
    )

    pdf = canvas.Canvas(response)

    y = 800

    pdf.drawString(
        220,
        y,
        "Accounts Report"
    )

    y -= 30

    for account in accounts:

        pdf.drawString(
            30,
            y,
            f"{account.account_number} | "
            f"{account.customer.first_name} "
            f"{account.customer.last_name} | "
            f"{account.account_type} | "
            f"{account.balance}"
        )

        y -= 20

        if y < 50:

            pdf.showPage()

            y = 800

    pdf.save()

    return response


# ==========================================
# Date Wise Report
# ==========================================

# ==========================================
# Date Wise Report
# ==========================================

@login_required
def account_report(request):

    start_date = request.GET.get("start_date", "")

    end_date = request.GET.get("end_date", "")

    accounts = Account.objects.select_related(
        "customer"
    )

    if start_date and end_date:

        accounts = accounts.filter(
            created_at__date__range=[
                start_date,
                end_date
            ]
        )

    total_balance = accounts.aggregate(
        total=Sum("balance")
    )["total"] or 0

    total_accounts = accounts.count()

    return render(
        request,
        "accounts/account_report.html",
        {
            "accounts": accounts,
            "start_date": start_date,
            "end_date": end_date,
            "total_balance": total_balance,
            "total_accounts": total_accounts,
        }
    )

  