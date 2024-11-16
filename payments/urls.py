from django.urls import path
from .views import payment_failed
from .pesapal_payments import pesapal_payment_ipn, pesapal_payment_callback

urlpatterns = [
     path('pesapal/ipn/', pesapal_payment_ipn, name='pesapal_payment_ipn'),
     path("payment-failed/<str:order_number>/", payment_failed, name="payment_failed"),
     path("pesapal/payment-callback/", pesapal_payment_callback, name="pesapal_payment_callback"),
]
