from pyexpat import model
from django.shortcuts import render

from api.views import ListSingleModelMixin
from gst.models import TaxDue
from gst.serializer import TaxDuesSerializer



class TaxDuesView(ListSingleModelMixin):
    model = TaxDue
    serializer_class = TaxDuesSerializer
    def get_queryset(self):
        return self.model.objects.all()