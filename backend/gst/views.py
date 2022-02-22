from pyexpat import model
from django.shortcuts import render

from api.views import ListCRUDAPIView
from gst.models import TaxDue
from gst.serializer import ProductTaxDetailsSerializer,TaxDuesSerializer



class TaxDuesView(ListCRUDAPIView):
    model = TaxDue
    serializer_class = TaxDuesSerializer

    def post(self, request, *args, **kwargs):
        self.serializer_class = TaxDuesSerializer
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()

