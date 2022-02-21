from rest_framework import serializers
from gst.models import ProductTaxDetails,ServiceTaxDetails,TaxDue

class TaxDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTaxDetails
        fields = '__all__'


class TaxDuesSerializer(serializers.ModelSerializer):
    taxdetails = TaxDetailsSerializer()
    class Meta:
        model = TaxDue
        fields = '__all__'