import csv

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Q, Sum

from openpyxl import Workbook
from reportlab.pdfgen import canvas

from .models import Employee
from .forms import EmployeeForm


# ==========================================
# Common Employee Query
# ==========================================

def get_filtered_employees(request):

    search = request.GET.get("search", "").strip()
    department = request.GET.get("department", "")
    status = request.GET.get("status", "")
    sort = request.GET.get("sort", "-created_at")

    employees = Employee.objects.all()

    if search:

        employees = employees.filter(
            Q(employee_id__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(department__icontains=search) |
            Q(designation__icontains=search) |
            Q(phone__icontains=search) |
            Q(email__icontains=search)
        )

    if department:
        employees = employees.filter(department=department)

    if status:
        employees = employees.filter(status=status)

    employees = employees.order_by(sort)

    return employees


# ==========================================
# Employee List
# ==========================================

@login_required
def employee_list(request):

    search = request.GET.get("search", "").strip()

    employees = get_filtered_employees(request)

    paginator = Paginator(employees, 10)

    page_number = request.GET.get("page")

    employees = paginator.get_page(page_number)

    return render(
        request,
        "employees/employees.html",
        {
            "employees": employees,
            "search": search,
            "department": request.GET.get("department", ""),
            "status": request.GET.get("status", ""),
            "sort": request.GET.get("sort", "-created_at"),
        }
    )


# ==========================================
# Add Employee
# ==========================================

@login_required
def add_employee(request):

    if request.method == "POST":

        form = EmployeeForm(request.POST)

        if form.is_valid():

            employee = form.save(commit=False)

            if employee.joining_date < employee.dob:

                messages.error(
                    request,
                    "Joining Date cannot be earlier than Date of Birth."
                )

            else:

                employee.save()

                messages.success(
                    request,
                    "Employee added successfully."
                )

                return redirect("employees")

        else:

            print(form.errors)

    else:

        form = EmployeeForm()

    return render(
        request,
        "employees/add_employees.html",
        {
            "form": form
        }
    )


# ==========================================
# Edit Employee
# ==========================================

@login_required
def edit_employee(request, id):

    employee = get_object_or_404(Employee, id=id)

    if request.method == "POST":

        form = EmployeeForm(
            request.POST,
            instance=employee
        )

        if form.is_valid():

            employee = form.save(commit=False)

            if employee.joining_date < employee.dob:

                messages.error(
                    request,
                    "Joining Date cannot be earlier than Date of Birth."
                )

            else:

                employee.save()

                messages.success(
                    request,
                    "Employee updated successfully."
                )

                return redirect("employees")

        else:

            print(form.errors)

    else:

        form = EmployeeForm(instance=employee)

    return render(
        request,
        "employees/edit_employees.html",
        {
            "form": form,
            "employee": employee
        }
    )


# ==========================================
# Delete Employee
# ==========================================

@login_required
def delete_employee(request, id):

    employee = get_object_or_404(
        Employee,
        id=id
    )

    if request.method == "POST":

        employee.delete()

        messages.success(
            request,
            "Employee deleted successfully."
        )

        return redirect("employees")

    return render(
        request,
        "employees/delete_employees.html",
        {
            "employee": employee
        }
    )


# ==========================================
# Export CSV
# ==========================================

@login_required
def export_employees_csv(request):

    employees = get_filtered_employees(request)

    response = HttpResponse(content_type="text/csv")

    response["Content-Disposition"] = 'attachment; filename="employees.csv"'

    writer = csv.writer(response)

    writer.writerow([
        "Employee ID",
        "Name",
        "Department",
        "Designation",
        "Phone",
        "Email",
        "Salary",
        "Status"
    ])

    for employee in employees:

        writer.writerow([
            employee.employee_id,
            employee.first_name + " " + employee.last_name,
            employee.department,
            employee.designation,
            employee.phone,
            employee.email,
            employee.salary,
            employee.status
        ])

    return response


# ==========================================
# Export Excel
# ==========================================

@login_required
def export_employees_excel(request):

    employees = get_filtered_employees(request)

    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Employees"

    sheet.append([
        "Employee ID",
        "Name",
        "Department",
        "Designation",
        "Phone",
        "Email",
        "Salary",
        "Status"
    ])

    for employee in employees:

        sheet.append([
            employee.employee_id,
            employee.first_name + " " + employee.last_name,
            employee.department,
            employee.designation,
            employee.phone,
            employee.email,
            float(employee.salary),
            employee.status
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = 'attachment; filename="employees.xlsx"'

    workbook.save(response)

    return response


# ==========================================
# Export PDF
# ==========================================

@login_required
def export_employees_pdf(request):

    employees = get_filtered_employees(request)

    response = HttpResponse(content_type="application/pdf")

    response["Content-Disposition"] = 'attachment; filename="employees.pdf"'

    pdf = canvas.Canvas(response)

    y = 800

    pdf.drawString(220, y, "Employee Report")

    y -= 30

    for employee in employees:

        pdf.drawString(
            30,
            y,
            f"{employee.employee_id} | "
            f"{employee.first_name} {employee.last_name} | "
            f"{employee.department} | "
            f"{employee.designation}"
        )

        y -= 20

        if y < 50:

            pdf.showPage()

            y = 800

    pdf.save()

    return response


# ==========================================
# Employee Report
# ==========================================

@login_required
def employee_report(request):

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    employees = Employee.objects.all()

    if start_date and end_date:

        employees = employees.filter(
            created_at__date__range=[
                start_date,
                end_date
            ]
        )

    total_employees = employees.count()

    total_salary = employees.aggregate(
        total=Sum("salary")
    )["total"] or 0

    return render(
        request,
        "employees/employee_report.html",
        {
            "employees": employees,
            "start_date": start_date,
            "end_date": end_date,
            "total_employees": total_employees,
            "total_salary": total_salary,
        }
    )