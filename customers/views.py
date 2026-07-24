import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from openpyxl import Workbook
from reportlab.pdfgen import canvas

from .forms import CustomerForm
from .models import Customer


# ==========================================
# Common Customer Query
# ==========================================

def get_filtered_customers(request):

    search = request.GET.get("search", "").strip()
    gender = request.GET.get("gender", "")
    status = request.GET.get("status", "")
    sort = request.GET.get("sort", "-customer_id")

    customers = Customer.objects.all()

    if search:
        customers = customers.filter(
            Q(customer_id__icontains=search)
            | Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(phone__icontains=search)
            | Q(email__icontains=search)
            | Q(city__icontains=search)
        )

    if gender:
        customers = customers.filter(gender=gender)

    if status:
        customers = customers.filter(status=status)

    customers = customers.order_by(sort)

    return customers


# ==========================================
# Customer List
# ==========================================

@login_required
def customer_list(request):

    search = request.GET.get("search", "").strip()

    customers = get_filtered_customers(request)

    paginator = Paginator(customers, 10)

    page_number = request.GET.get("page")

    customers = paginator.get_page(page_number)

    return render(
        request,
        "customers/customers.html",
        {
            "customers": customers,
            "search": search,
            "gender": request.GET.get("gender", ""),
            "status": request.GET.get("status", ""),
            "sort": request.GET.get("sort", "-customer_id"),
        },
    )


# ==========================================
# Add Customer
# ==========================================

@login_required
def add_customer(request):

    if request.method == "POST":

        form = CustomerForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Customer added successfully.",
            )

            return redirect("customers")

        else:
            print(form.errors)

    else:
        form = CustomerForm()

    return render(
        request,
        "customers/add_customers.html",
        {
            "form": form,
        },
    )


# ==========================================
# Edit Customer
# ==========================================

@login_required
def edit_customer(request, id):

    customer = get_object_or_404(
        Customer,
        id=id,
    )

    if request.method == "POST":

        form = CustomerForm(
            request.POST,
            instance=customer,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Customer updated successfully.",
            )

            return redirect("customers")

    else:

        form = CustomerForm(
            instance=customer,
        )

    return render(
        request,
        "customers/edit_customers.html",
        {
            "form": form,
            "customer": customer,
        },
    )


# ==========================================
# Delete Customer
# ==========================================

@login_required
def delete_customer(request, id):

    customer = get_object_or_404(
        Customer,
        id=id,
    )

    if request.method == "POST":

        customer.delete()

        messages.success(
            request,
            "Customer deleted successfully.",
        )

        return redirect("customers")

    return render(
        request,
        "customers/delete_customers.html",
        {
            "customer": customer,
        },
    )


# ==========================================
# Export CSV
# ==========================================

@login_required
def export_customers_csv(request):

    customers = get_filtered_customers(request)

    response = HttpResponse(content_type="text/csv")

    response["Content-Disposition"] = (
        'attachment; filename="customers.csv"'
    )

    writer = csv.writer(response)

    writer.writerow(
        [
            "Customer ID",
            "Name",
            "Gender",
            "Phone",
            "Email",
            "City",
            "Status",
        ]
    )

    for customer in customers:
        writer.writerow(
            [
                customer.customer_id,
                f"{customer.first_name} {customer.last_name}",
                customer.gender,
                customer.phone,
                customer.email,
                customer.city,
                customer.status,
            ]
        )

    return response


# ==========================================
# Export Excel
# ==========================================

@login_required
def export_customers_excel(request):

    customers = get_filtered_customers(request)

    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Customers"

    sheet.append(
        [
            "Customer ID",
            "Name",
            "Gender",
            "Phone",
            "Email",
            "City",
            "Status",
        ]
    )

    for customer in customers:
        sheet.append(
            [
                customer.customer_id,
                f"{customer.first_name} {customer.last_name}",
                customer.gender,
                customer.phone,
                customer.email,
                customer.city,
                customer.status,
            ]
        )

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = (
        'attachment; filename="customers.xlsx"'
    )

    workbook.save(response)

    return response


# ==========================================
# Export PDF
# ==========================================

@login_required
def export_customers_pdf(request):

    customers = get_filtered_customers(request)

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        'attachment; filename="customers.pdf"'
    )

    pdf = canvas.Canvas(response)

    y = 800

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, y, "Customer Report")

    y -= 30

    pdf.setFont("Helvetica", 10)

    for customer in customers:

        pdf.drawString(
            30,
            y,
            f"{customer.customer_id} | "
            f"{customer.first_name} {customer.last_name} | "
            f"{customer.phone} | "
            f"{customer.city}"
        )

        y -= 20

        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y = 800

    pdf.save()

    return response


# ==========================================
# Customer Report
# ==========================================

@login_required
def customer_report(request):

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    customers = Customer.objects.all()

    if start_date and end_date:
        customers = customers.filter(
            created_at__date__range=[
                start_date,
                end_date,
            ]
        )

    total_customers = customers.count()

    return render(
        request,
        "customers/customer_report.html",
        {
            "customers": customers,
            "start_date": start_date,
            "end_date": end_date,
            "total_customers": total_customers,
        },
    )