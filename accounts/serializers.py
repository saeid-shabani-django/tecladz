from djoser.serializers import UserCreateSerializer as DjangoUserCreateSerializer
from djoser.serializers import UserSerializer as DjangoUserSerializer
from .models import CustomUser
class UserCreateSerializer(DjangoUserCreateSerializer):
    class Meta:
        model = CustomUser
        fields=['email','password']


class UserSerializer(DjangoUserSerializer):
    class Meta(DjangoUserSerializer.Meta):
        fields=['id','user','first_name']