from django.contrib import admin
from django.urls import path
from users.views import test_logging, transactions, prices, RegisterView, LoginView, RoleView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', test_logging),
    path('api/v1/transactions', transactions, name='transactions'),
    path('api/v1/prices', prices, name='prices'),
    path('api/v1/auth/register', RegisterView.as_view(), name='register'),
    path('api/v1/auth/login', LoginView.as_view(), name='login'),
    path('api/v1/role', RoleView.as_view(), name='role'),

]
