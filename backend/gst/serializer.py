from django.forms import ValidationError
from rest_framework import serializers
from users.models import TaxAccountant
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

class AbstractTaxDuesSerializer(serializers.ModelSerializer):
    product_taxdetails = ProductTaxDetailsSerializer(many=True)
    service_taxdetails = ServiceTaxDetailsSerializer(many=True) 

    class Meta:
        model = TaxDue
        read_only_fields = ("cgst","sgst","ugst","igst","cess","total","generatedon","editedon")
        extra_kwargs ={"generatedby": {'write_only': True,'required':False}}
        fields = '__all__'

class CreateTaxDuesSerializer(AbstractTaxDuesSerializer):

    def create(self, validated_data):
        product_taxdetails = None
        service_taxdetails = None
        if not 'generatedby' in validated_data:
            if type(self.context["request"].user) is TaxAccountant:
                validated_data['generatedby'] = self.context["request"].user
            else:
                raise ValidationError('generatedby is required')
        if 'product_taxdetails' in validated_data:
            product_taxdetails =  validated_data.pop("product_taxdetails")
        if 'service_taxdetails' in validated_data:
            service_taxdetails = validated_data.pop("service_taxdetails")
        taxdue:TaxDue = super().create(validated_data)
        taxdue.CalculateTaxDue(product_taxdetails,service_taxdetails)
        self.instance = taxdue
        return taxdue
    def update(self, instance, validated_data):
        product_taxdetails = None
        service_taxdetails = None
        if 'product_taxdetails' in validated_data:
            product_taxdetails =  validated_data.pop("product_taxdetails")
        if 'service_taxdetails' in validated_data:
            service_taxdetails = validated_data.pop("service_taxdetails")
        taxdue:TaxDue = super().update(instance, validated_data)
        if product_taxdetails:
            for product_taxdetail,instance_product_taxdetail in zip(product_taxdetails,instance.product_taxdetails.all()):
                for attr, value in product_taxdetail.items():
                    setattr(instance_product_taxdetail, attr, value)
                    instance_product_taxdetail.save()
        if service_taxdetails:
            for service_taxdetail,instance_service_taxdetail in zip(service_taxdetails,instance.service_taxdetails.all()):
                for attr, value in service_taxdetail.items():
                    setattr(instance_service_taxdetail, attr, value)
                    instance_service_taxdetail.save()
        taxdue.Recalculate()
        return taxdue

