from django.urls import path
from . import views

urlpatterns = [
    path('crypto_price_checker/', views.crypto_price_checker, name='crypto_price_checker'),

]
