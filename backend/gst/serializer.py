from rest_framework import serializers

class TaxDuesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'