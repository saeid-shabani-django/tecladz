from django.urls import path
from . import views



urlpatterns =[
    path('process/',views.payment,name='payment'),
    path('callback/',views.payment_callback_view,name='payment_callback'),
]






