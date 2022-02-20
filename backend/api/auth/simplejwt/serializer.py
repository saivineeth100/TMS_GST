from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as baseTokenObtainSerializer
from .token import RefreshToken

class TokenObtainPairSerializer(baseTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    