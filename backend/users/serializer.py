from rest_framework import serializers

from users.models import TaxPayer, TaxAccountant,AdminUser


class GenericUserSerializer(serializers.ModelSerializer):
    class Meta:
    
        read_only_fields = ("is_active", "is_staff", "is_superuser", "date_joined","last_login","user_permissions")
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
        }
        exclude = ["groups"]
        #fields = '__all__'

class AdminUserSerializer(GenericUserSerializer):
    class Meta(GenericUserSerializer.Meta):
        model = AdminUser

class TaxPayerSerializer(GenericUserSerializer):
    class Meta(GenericUserSerializer.Meta):
        model = TaxPayer

class TaxAccountantSerializer(GenericUserSerializer):
    class Meta(GenericUserSerializer.Meta):
        model = TaxAccountant