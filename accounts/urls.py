from django.urls import path
from .views import register_author, register_customer

urlpatterns = [
    path('register/author', register_author, name='register_author'),
    path('register/customer', register_customer, name='register_customer'),
]