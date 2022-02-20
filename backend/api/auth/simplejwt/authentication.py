from django.utils.translation import gettext_lazy as _

from rest_framework_simplejwt.authentication import JWTAuthentication as baseauth
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError

from users.models import AdminUser, TaxPayer,TaxAccountant

class JWTAuthentication(baseauth):

    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
            modeltype = validated_token["modeltype"]
            if modeltype == "AdminUser":
                self.user_model = AdminUser
            if modeltype == "TaxAccountant":
                self.user_model = TaxAccountant
            if modeltype == "TaxPayer":
                self.user_model = TaxPayer
        except KeyError:
            raise InvalidToken(
                _('Token contained no recognizable user identification'))

        try:
            user = self.user_model.objects.get(
                **{api_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed(
                _('User not found'), code='user_not_found')

        if not user.is_active:
            raise AuthenticationFailed(
                _('User is inactive'), code='user_inactive')

        return user
