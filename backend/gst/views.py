from pyexpat import model
from django.shortcuts import render

from api.views import ListCRUDAPIView
from gst.models import TaxDue
from users.models import TaxAccountant,AdminUser
from gst.serializer import ProductTaxDetailsSerializer,CreateTaxDuesSerializer


from rest_framework.exceptions import PermissionDenied

class TaxDuesView(ListCRUDAPIView):
    model = TaxDue
    serializer_class = CreateTaxDuesSerializer

    def post(self, request, *args, **kwargs):
        self.serializer_class = CreateTaxDuesSerializer
        
        return super().post(request, *args, **kwargs)
    
    def get_queryset(self):
        self.user = self.request.user
        self.user_type = type(self.user)
        if self.user_type is AdminUser or self.user_type  is TaxAccountant:
            if self.user_type is TaxAccountant:
                return self.user.clienttaxdues.all()
            else:
                self.model.objects.all()
        else:
            raise PermissionDenied

