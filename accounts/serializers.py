from djoser.serializers import UserCreateSerializer as DjangoUserCreateSerializer
from djoser.serializers import UserSerializer as DjangoUserSerializer

class UserCreateSerializer(DjangoUserCreateSerializer):
    class Meta(DjangoUserCreateSerializer.Meta):
        fields=['email','password']


class UserSerializer(DjangoUserSerializer):
    class Meta(DjangoUserSerializer.Meta):
        fields=['id','user','first_name']