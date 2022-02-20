# External

from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView

#from api.auth.simplejwt.serializer import TokenObtainPairSerializer
from api.auth.serializer import TokenVerifySerializer, ChangePasswordSerializer,SignUpSerializer
from users.models import AdminUser
from users.serializer import AdminUserSerializer
from users.serializer import TaxAccountantSerializer
from users.models import TaxAccountant,TaxPayer
from users.serializer import TaxPayerSerializer

from api.auth.simplejwt.serializer import TokenObtainPairSerializer

class LoginView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    mapping = {
        AdminUser:AdminUserSerializer,
        TaxAccountant:TaxAccountantSerializer,
        TaxPayer:TaxPayerSerializer,
    }
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            usermodel = type(serializer.user)
            userdata = self.mapping.get(usermodel)(serializer.user).data
        except TokenError as e:
            raise InvalidToken(e.args[0])
        response = Response(
            {
                "tokens": {**serializer.validated_data},
                "user": {**userdata},
            },
            status=status.HTTP_200_OK,
        )
        return response
