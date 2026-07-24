from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse

import csv

from openpyxl import Workbook
from reportlab.pdfgen import canvas

from django.db.models import Q, Sum

from .models import Loan
from .forms import LoanForm


# =====================================
# Common Loan Query
# =====================================

def get_filtered_loans(request):

    search = request.GET.get("search", "").strip()

    loan_type = request.GET.get("loan_type", "")

    status = request.GET.get("status", "")

    sort = request.GET.get("sort", "-created_at")

    loans = Loan.objects.select_related(
        "customer",
        "account"
    )

    if search:

        loans = loans.filter(
            Q(loan_number__icontains=search) |
            Q(customer__customer_id__icontains=search) |
            Q(customer__first_name__icontains=search) |
            Q(customer__last_name__icontains=search) |
            Q(account__account_number__icontains=search)
        )

    if loan_type:

        loans = loans.filter(
            loan_type=loan_type
        )

    if status:

        loans = loans.filter(
            status=status
        )

    loans = loans.order_by(sort)

    return loans


# =====================================
# Loan List
# =====================================

@login_required
def loan_list(request):

    loans = get_filtered_loans(request)

    paginator = Paginator(loans, 10)

    page_number = request.GET.get("page")

    loans = paginator.get_page(page_number)

    return render(
        request,
        "loans/loans.html",
        {
            "loans": loans,
            "search": request.GET.get("search", ""),
            "loan_type": request.GET.get("loan_type", ""),
            "status": request.GET.get("status", ""),
            "sort": request.GET.get("sort", "-created_at"),
        }
    )


# =====================================
# Add Loan
# =====================================

@login_required
def add_loan(request):

    if request.method == "POST":

        form = LoanForm(request.POST)

        if form.is_valid():

            loan = form.save(commit=False)

            if loan.end_date <= loan.start_date:

                messages.error(
                    request,
                    "End Date must be greater than Start Date."
                )

            else:

                loan.save()

                messages.success(
                    request,
                    "Loan added successfully."
                )

                return redirect("loans")

        else:

            print(form.errors)

    else:

        form = LoanForm()

    return render(
        request,
        "loans/add_loan.html",
        {
            "form": form
        }
    )


# =====================================
# Edit Loan
# =====================================

@login_required
def edit_loan(request, id):

    loan = get_object_or_404(
        Loan,
        id=id
    )

    if request.method == "POST":

        form = LoanForm(
            request.POST,
            instance=loan
        )

        if form.is_valid():

            loan = form.save(commit=False)

            if loan.end_date <= loan.start_date:

                messages.error(
                    request,
                    "End Date must be greater than Start Date."
                )

            else:

                loan.save()

                messages.success(
                    request,
                    "Loan updated successfully."
                )

                return redirect("loans")

        else:

            print(form.errors)

    else:

        form = LoanForm(
            instance=loan
        )

    return render(
        request,
        "loans/edit_loan.html",
        {
            "form": form,
            "loan": loan
        }
    )


# =====================================
# Delete Loan
# =====================================

@login_required
def delete_loan(request, id):

    loan = get_object_or_404(
        Loan,
        id=id
    )

    if request.method == "POST":

        loan.delete()

        messages.success(
            request,
            "Loan deleted successfully."
        )

        return redirect("loans")

    return render(
        request,
        "loans/delete_loan.html",
        {
            "loan": loan
        }
    )
# =====================================
# Export Loans - CSV
# =====================================

@login_required
def export_loans_csv(request):

    loans = get_filtered_loans(request)

    response = HttpResponse(content_type="text/csv")

    response["Content-Disposition"] = 'attachment; filename="loans.csv"'

    writer = csv.writer(response)

    writer.writerow([
        "Loan Number",
        "Customer",
        "Account Number",
        "Loan Type",
        "Loan Amount",
        "EMI",
        "Status"
    ])

    for loan in loans:

        writer.writerow([
            loan.loan_number,
            f"{loan.customer.first_name} {loan.customer.last_name}",
            loan.account.account_number,
            loan.loan_type,
            loan.loan_amount,
            loan.emi,
            loan.status
        ])

    return response


# =====================================
# Export Loans - Excel
# =====================================

@login_required
def export_loans_excel(request):

    loans = get_filtered_loans(request)

    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Loans"

    sheet.append([
        "Loan Number",
        "Customer",
        "Account Number",
        "Loan Type",
        "Loan Amount",
        "EMI",
        "Status"
    ])

    for loan in loans:

        sheet.append([
            loan.loan_number,
            f"{loan.customer.first_name} {loan.customer.last_name}",
            loan.account.account_number,
            loan.loan_type,
            float(loan.loan_amount),
            float(loan.emi),
            loan.status
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = 'attachment; filename="loans.xlsx"'

    workbook.save(response)

    return response


# =====================================
# Export Loans - PDF
# =====================================

@login_required
def export_loans_pdf(request):

    loans = get_filtered_loans(request)

    response = HttpResponse(content_type="application/pdf")

    response["Content-Disposition"] = 'attachment; filename="loans.pdf"'

    pdf = canvas.Canvas(response)

    y = 800

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(220, y, "Loan Report")

    y -= 30

    pdf.setFont("Helvetica", 10)

    for loan in loans:

        pdf.drawString(
            30,
            y,
            f"{loan.loan_number} | "
            f"{loan.customer.first_name} {loan.customer.last_name} | "
            f"{loan.loan_type} | "
            f"₹ {loan.loan_amount} | "
            f"{loan.status}"
        )

        y -= 20

        if y < 50:

            pdf.showPage()

            pdf.setFont("Helvetica", 10)

            y = 800

    pdf.save()

    return response


# =====================================
# Loan Report
# =====================================

@login_required
def loan_report(request):

    start_date = request.GET.get("start_date")

    end_date = request.GET.get("end_date")

    loans = Loan.objects.select_related(
        "customer",
        "account"
    )

    if start_date and end_date:

        loans = loans.filter(
            created_at__date__range=[
                start_date,
                end_date
            ]
        )

    total_loans = loans.count()

    total_amount = loans.aggregate(
        total=Sum("loan_amount")
    )["total"] or 0

    return render(
        request,
        "loans/loan_report.html",
        {
            "loans": loans,
            "start_date": start_date,
            "end_date": end_date,
            "total_loans": total_loans,
            "total_amount": total_amount,
        }
    )