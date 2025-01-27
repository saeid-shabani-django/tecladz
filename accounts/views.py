from rest_framework.response import Response
from rest_framework.views import APIView
from djoser.conf import settings as djoser_settings
from .tasks import send_activation_email
from django.conf import settings
import jwt
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from djoser.utils import decode_uid
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework import status
from .models import CustomUser
from django.urls import reverse
import datetime
from djoser import utils

class CustomRegistrationView(APIView):
   def post(self, request):
        serializer = djoser_settings.SERIALIZERS.user_create(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(is_active=False)

        
        uid = utils.encode_uid(user.pk)
        token = djoser_settings.TOKEN_GENERATOR.make_token(user)

        activation_link = request.build_absolute_uri(
            reverse('activation', kwargs={'uid': uid, 'token': token})  # ← Correct reversal
        )

        send_activation_email.delay(user.email, activation_link)
        return Response(status=status.HTTP_201_CREATED)

class ActivationView(APIView):
    def get(self, request, uid, token):
        try:
           
            response = self.activate_user(uid, token)
            if response.status_code == status.HTTP_204_NO_CONTENT:
                return redirect('login')  # Or 'jwt-create' if using JWT
            return Response("Activation failed", status=response.status_code)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def activate_user(self, uid, token):
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        
        
        request = factory.post(
            '/auth/users/activation/',  
            data={'uid': uid, 'token': token},
            format='json'
        )
        return UserViewSet.as_view({'post': 'activation'})(request)
    