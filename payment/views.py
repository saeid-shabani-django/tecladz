from store.models import Order
from django.shortcuts import get_object_or_404,redirect,reverse
from rest_framework import status
from rest_framework.response import Response
import requests
import json



def payment(request):
    customer_id = request.user.id
    order_id = Order.objects.get(customer_id=customer_id).id
    order = get_object_or_404(Order,id=order_id)
    total_price = order.get_total_price()

    zarinpal_request_for_post = (
        "https://payment.zarinpal.com/pg/v4/payment/request.json"
    )


    request_data = {
        "merchant_id": "07d2feec-2010-4bb2-a380-f0f4d4075453",
        "amount": total_price,
        "callback_url": reverse('payment_callback'),
        "description": f"tecladz transaction for the user:  {request.user.username}",
        "metadata": {"mobile": "09109555234", "email": "info.test@example.com"},
    }
    header = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    resp = requests.post(
        url=zarinpal_request_for_post,
        data=json.dumps(
            request_data),
        headers=header,
        timeout=10
    )
    data = resp.json()["data"]
    authority = data["authority"]
    order.authority_from_zarinpal = authority
    order.save()
    if (len(resp.json()["errors"] == 0)) or (not resp.json()["errors"]):
        return redirect(f"https://sandbox.zarinpal.com/pg/StartPay/{authority}")
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

def payment_callback_view(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')
    order = get_object_or_404(Order,authority_from_zarinpal = payment_authority)
    total_price = order.get_total_price()
    if payment_status=='OK':
        header = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        }
        request_data = {
        "merchant_id": "07d2feec-2010-4bb2-a380-f0f4d4075453",
        "amount": total_price,
        "authority":payment_authority
        }
        resp = requests.post(url='https://sandbox.zarinpal.com/pg/v4/payment/verify.json',data=json.dumps(request_data),headers=header)
        data = resp.json()["data"]
        if 'data' in resp.json() and (len(resp.json()["data"]["errors"] == 0)) or (not resp.json()["data"]["errors"]):
            data = resp.json()["data"]
            payment_code = data['code']
            if payment_code == 100:
                order.status = 'paid'
                order.ref_id_from_zarinpal = data['ref_id']
                order.data_from_zarinpal = data
                order.save()
return Response('the payment process was successful',status=status.HTTP_200_OK)
            elif payment_code == 101:
                return Response('the payment has been proceed before',status=status.HTTP_200_OK)
            else:
                error_code = resp.json()['errors']['code']
                error_message = resp.json()['errors']['message']
                return Response(f'{error_message} {error_code}',status=status.HTTP_401_UNAUTHORIZED)




