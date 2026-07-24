from django.contrib import admin
from django.urls import path, include
from .views import index

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='home'),

    path('accounts/', include('accounts.urls')),
    path('customers/', include('customers.urls')),
    path('transactions/', include('transactions.urls')),
    path('loans/', include('loans.urls')),
    path('employees/', include('employees.urls')),
    path('auth/', include('authentication.urls')),
]