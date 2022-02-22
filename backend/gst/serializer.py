from rest_framework import serializers
from gst.models import ProductTaxDetails,ServiceTaxDetails,TaxDue

class AbstractTaxDetilsSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ["taxdue"]
        #fields = '__all__'

class ProductTaxDetailsSerializer(AbstractTaxDetilsSerializer):
    class Meta(AbstractTaxDetilsSerializer.Meta):
        model = ProductTaxDetails

class ServiceTaxDetailsSerializer(AbstractTaxDetilsSerializer):
    class Meta(AbstractTaxDetilsSerializer.Meta):
        model = ServiceTaxDetails

class TaxDuesSerializer(serializers.ModelSerializer):
    product_taxdetails = ProductTaxDetailsSerializer(many=True)
    service_taxdetails = ServiceTaxDetailsSerializer(many=True)
    
    class Meta:
        model = TaxDue
        read_only_fields = ("cgst","sgst","ugst","igst","cess","total")
        fields = '__all__'