# 🏦 Banking Management System — Django

A web-based Banking Management System built with **Django** and **Python** to automate and simplify day-to-day banking operations — customers, accounts, employees, loans, and transactions — through a single, secure, centralized platform.

🔗 **Live Demo:** [banking-management-system-django.onrender.com](https://banking-management-system-django.onrender.com/)
📂 **Repository:** [github.com/Nandu-ai2/Banking-Management-System-Django](https://github.com/Nandu-ai2/Banking-Management-System-Django)

> ⚠️ Note: The app is hosted on Render's free tier, so the live demo may take 30–60 seconds to wake up on first load.

---

## 📖 Overview

The Banking Management System replaces manual, paper-based record-keeping with a centralized Django web application. It gives administrators a secure dashboard to manage customers, accounts, employees, loans, and transactions, complete with authentication, reporting, and a responsive Bootstrap UI.

**Goals:**
- Improve banking efficiency and reduce paperwork
- Keep customer and financial data secure and centralized
- Give admins fast, CRUD-based control over every banking entity
- Provide clear, exportable reports and at-a-glance statistics

---

## ✨ Features

- 🔐 **Authentication** — Secure login/logout via Django's built-in auth system
- 👤 **Customer Management** — Add, edit, delete, and search customer records
- 💳 **Account Management** — Create and maintain bank accounts with balance tracking
- 🧑‍💼 **Employee Management** — Manage employee and administrative records
- 💰 **Loan Management** — Record and track customer loans
- 🔄 **Transaction Management** — Log deposits, withdrawals, and full transaction history
- 📊 **Dashboard** — Live stats: total customers, accounts, employees, loans, transactions, and bank balance
- 📄 **Reports** — Export data as **CSV**, **Excel**, and **PDF**
- 🔍 **Search & Pagination** — Fast lookups across large datasets
- 📱 **Responsive UI** — Built with Bootstrap for desktop, tablet, and mobile

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Backend Framework | Django |
| Frontend | HTML5, CSS3, Bootstrap, JavaScript |
| Database (Dev) | SQLite |
| Database (Prod) | PostgreSQL |
| Report Generation | OpenPyXL (Excel), ReportLab (PDF) |
| Version Control | Git & GitHub |
| Deployment | Render |

---

## 📁 Project Structure

```
Banking-Management-System-Django/
├── accounts/         # Account creation & balance management
├── authentication/   # Login, logout & user auth
├── bank/             # Core project settings & URL routing
├── customers/        # Customer CRUD & search
├── employees/        # Employee records management
├── loans/             # Loan records management
├── transactions/     # Deposits, withdrawals & transaction history
├── static/           # CSS, JS, and static assets
├── templates/        # HTML templates (Bootstrap-based UI)
├── db.sqlite3         # Development database
├── requirements.txt   # Python dependencies
└── manage.py           # Django management script
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- pip
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Nandu-ai2/Banking-Management-System-Django.git
cd Banking-Management-System-Django

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create an admin/superuser account
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

Then open **http://127.0.0.1:8000/** in your browser (admin panel at **/admin**).

### Production Notes
- Swap `SQLite` for `PostgreSQL` by updating `DATABASES` in settings and setting the appropriate environment variables.
- Set `DEBUG = False` and configure `ALLOWED_HOSTS` before deploying.
- The live version of this project is deployed on **Render**.

---

## 🔮 Future Enhancements

- Full online/self-service banking for end customers
- SMS & email notifications for transactions
- AI-based fraud detection
- UPI payment integration
- Native mobile application support

---

## 📄 License

This project is available for educational and personal use. Feel free to fork and build on it.

---

## 🙋 Author

**Nandu-ai2** — [GitHub Profile](https://github.com/Nandu-ai2)
