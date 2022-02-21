from pyexpat import model
from django.shortcuts import render

from api.views import CRUDAPIView
from gst.models import TaxDue
from gst.serializer import TaxDetailsSerializer,TaxDuesSerializer



class TaxDuesView(CRUDAPIView):
    model = TaxDue
    serializer_class = TaxDetailsSerializer

    def post(self, request, *args, **kwargs):
        self.serializer_class = TaxDetailsSerializer
        return super().post(request, *args, **kwargs)
    def get_queryset(self):
        return self.model.objects.all()

