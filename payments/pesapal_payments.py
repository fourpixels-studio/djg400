import json
import time
import logging
import requests
from django.conf import settings
from django.utils import timezone
from orders.models import Order
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_variables

logger = logging.getLogger('django')


@sensitive_variables('PESAPAL_CONSUMER_KEY', 'PESAPAL_CONSUMER_SECRET')
class PesaPal:
    def __init__(self):
        self.base_url = 'https://pay.pesapal.com/v3/api/'

        self.payload = json.dumps({
            "consumer_key": settings.PESAPAL_CONSUMER_KEY,
            "consumer_secret": settings.PESAPAL_CONSUMER_SECRET,
        })

    def authenticate(self):
        endpoint = "Auth/RequestToken"

        headers = {
            "Content-Type": 'application/json',
            "Accept": 'application/json',
        }

        response = requests.request(
            "POST", self.base_url+endpoint, headers=headers, data=self.payload)

        return response.json()['token']

    def registerIPN_URL(self):
        endpoint = "URLSetup/RegisterIPN"
        myIPN_url = f'{settings.SITE_DOMAIN}pesapal/ipn/'

        payload = json.dumps({
            "url": myIPN_url,
            "ipn_notification_type": "POST",
        })

        headers = {
            "Accept": 'application/json',
            "Content-Type": 'application/json',
            "Authorization": self.authenticate(),
        }

        response = requests.request(
            "POST", self.base_url+endpoint, headers=headers, data=payload)

        return response.json()

    def submit_order(self, order, description):
        endpoint = "Transactions/SubmitOrderRequest"

        callback_url = f'{settings.SITE_DOMAIN}pesapal/payment-callback/'
        cancellation_url = f'{settings.SITE_DOMAIN}payment-failed/{order.order_number}/'

        payload = json.dumps({
            "id": order.order_number,
            "currency": "KES",
            "amount": order.amount,
            "description": description,
            "callback_url": callback_url,
            "cancellation_url": cancellation_url,
            "notification_id": self.registerIPN_URL()['ipn_id'],
            "billing_address": {
                "email_address": order.get_email,
                "phone_number": order.phone_number,
                "first_name": order.first_name,
                "middle_name": "",
                "last_name": order.last_name,
                "line_1": "",
                "line_2": "",
                "city": "",
                "state": "",
                "postal_code": None,
                "zip_code": None,
            }
        })

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": self.authenticate(),
        }

        response = requests.post(
            self.base_url + endpoint,
            headers=headers, data=payload
        )

        response_data = response.json()

        if 'order_tracking_id' in response_data and 'redirect_url' in response_data:
            return response_data
        else:
            raise KeyError(
                "The response from Pesapal does not contain 'order_tracking_id' or 'redirect_url'.")

    def check_transaction(self, tracking_id):
        timeout = time.time() + 60
        while time.time() < timeout:
            endpoint = f'Transactions/GetTransactionStatus?orderTrackingId={tracking_id}'
            headers = {
                "Accept": 'application/json',
                "Content-Type": 'application/json',
                "Authorization": self.authenticate(),
            }
            response = requests.get(self.base_url + endpoint, headers=headers)

            if response.status_code == 200:
                return response.json()
            else:
                print("Wrong transaction ID")
            time.sleep(5)

        raise Exception("Transaction status check timed out.")


@csrf_exempt
def pesapal_payment_callback(request):
    try:
        order_tracking_id = request.GET.get('OrderTrackingId')
        order_merchant_reference = request.GET.get('OrderMerchantReference')
        order = Order.objects.get(order_number=order_merchant_reference)
        pesapal = PesaPal()
        transaction_data = pesapal.check_transaction(order_tracking_id)
        status = transaction_data['payment_status_description']
        if status == 'Completed':
            if transaction_data['confirmation_code']:
                order.mpesa_code = transaction_data['confirmation_code']
            order.paid = True
            order.status = 'Completed'
            order.payment_date = transaction_data['created_date']
            order.save()
            return redirect('view_order', order.order_number)
        else:
            status = transaction_data['payment_status_description']
            order.paid = False
            order.status = f'Failed: {status}'
            order.save()
            return redirect('payment_failed', order.order_number)
    except:
        return HttpResponse("Invalid request", order=405)


@csrf_exempt
def pesapal_payment_ipn(request):
    if request.method == 'POST':
        order_tracking_id = request.POST.get('OrderTrackingId')
        merchant_reference = request.POST.get('OrderMerchantReference')
        notification_type = request.POST.get('OrderNotificationType')
        if notification_type == 'IPNCHANGE':
            pesapal = PesaPal()
            transaction_status = pesapal.check_transaction(order_tracking_id)
            try:
                order = Order.objects.get(order_number=merchant_reference)
                if transaction_status['status'] == 'COMPLETED':
                    order.paid = True
                    order.status = 'Paid'
                    order.order_tracking_id = order_tracking_id
                    order.payment_date = timezone.now()
                    order.save()
                    return HttpResponse("IPN handled", status=200)
            except Order.DoesNotExist:
                return HttpResponse("Ticket not found", status=404)
        return HttpResponse("Invalid IPN request", status=400)
    return HttpResponse(status=405)
