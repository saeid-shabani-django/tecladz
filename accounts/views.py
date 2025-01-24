from rest_framework.response import Response
from rest_framework.views import APIView
from djoser.conf import settings as djoser_settings
from .tasks import send_activation_email
from django.conf import settings
import jwt
from rest_framework import status
from .models import CustomUser
from django.urls import reverse
import datetime
class CustomRegistrationView(APIView):
    def post(self, request):
        
        
        serializer = djoser_settings.SERIALIZERS.user_create(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(is_active=False)
        
        
        activation_token = jwt.encode(
            {
                'user_id': user.id,
                'email': user.email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)  
            },
            settings.SECRET_KEY,
            algorithm='HS256'
        )
        
        
        activation_path = reverse('activation', kwargs={'token': activation_token})
        activation_link = request.build_absolute_uri(activation_path)
        activation_path = reverse('activation', kwargs={'token': activation_token})
        activation_link = request.build_absolute_uri(activation_path)
        
        send_activation_email.delay(user.email, activation_link)
        return Response(status=status.HTTP_201_CREATED)

class ActivationView(APIView):
    def get(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = CustomUser.objects.get(id=payload['user_id'], email=payload['email'])
            user.is_active = True
            user.save()
            return Response({'detail': 'Account activated'}, status=status.HTTP_200_OK)
        except (jwt.ExpiredSignatureError, jwt.DecodeError, CustomUser.DoesNotExist):
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)