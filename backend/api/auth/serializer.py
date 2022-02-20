from django.contrib.auth import password_validation

from rest_framework import serializers
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework.exceptions import ValidationError




if api_settings.BLACKLIST_AFTER_ROTATION:
    from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken


class TokenVerifySerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        token = UntypedToken(attrs['token'])

        if api_settings.BLACKLIST_AFTER_ROTATION:
            jti = token.get(api_settings.JTI_CLAIM)
            if BlacklistedToken.objects.filter(token__jti=jti).exists():
                raise ValidationError("Token is blacklisted")

        return {"status": "Valid Token"}


class ChangePasswordSerializer(serializers.Serializer):
    helptexts = password_validation.password_validators_help_texts()
    oldpassword = serializers.CharField(help_text=helptexts)
    new_password1 = serializers.CharField(help_text=helptexts)
    new_password2 = serializers.CharField(help_text=helptexts)
    user = None

    def is_valid(self, raise_exception=False):

        self.user = self.context.get("request").user
        super().is_valid(raise_exception=raise_exception)
        old_password = self._validated_data.get("oldpassword")
        if not self.user.check_password(old_password):
            raise serializers.ValidationError(
                detail={"error": "password_incorrect"},
                code='password_incorrect',
            )
        password1 = self._validated_data.get('new_password1')
        password2 = self._validated_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise serializers.ValidationError(
                    detail={"error": "password_mismatch"},
                    code='password_mismatch',
                )
        try:
            password_validation.validate_password(password2, self.user)
        except Exception as err:
            raise serializers.ValidationError(
                detail={"errors":err.messages},
                code='password_error',
            )

        return not bool(self._errors)

    def set_password(self, **kwargs):
        self.user.set_password(self._validated_data.get('new_password1'))
        self.user.save()

class SignUpSerializer(serializers.Serializer):
    helptexts = password_validation.password_validators_help_texts()
    username = serializers.CharField(min_length=5)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8,help_text=helptexts)
    password2 = serializers.CharField(min_length=8,help_text=helptexts)
    agreeterms = serializers.BooleanField(required=True)

    def is_valid(self, raise_exception=False):
        super().is_valid(raise_exception=raise_exception)
        password = self._validated_data.get('password')
        password2 = self._validated_data.get('password2')
        agreeterms = self._validated_data.get('agreeterms')
        if agreeterms is False:
            raise serializers.ValidationError(
                detail={"error": "Must Agree terms to Signup"},
                code='TermsnotAccepted',
            )
        if password != password2:
            raise serializers.ValidationError(
                detail={"error": "password_mismatch"},
                code='password_mismatch',
            )
        return not bool(self._errors)

    def addnewuser(self):
        username = self._validated_data.get('username')
        email = self._validated_data.get('email')
        password = self._validated_data.get('password')
        agreeterms = self._validated_data.get('agreeterms')

        # user = User(username=username,email=email)
        # user.set_password(password)
        # user.save()
    
