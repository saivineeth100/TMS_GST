

import django
from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin


from api.views import ListSingleModelMixin,ListCRUDAPIView
from users.models import TaxPayer, TaxAccountant,AdminUser
from users.serializer import TaxPayerSerializer,TaxAccountantSerializer

#List, view and edit  tax-payers - this can only be done by "tax-accountant" and "admin" roles
class TaxPayersAPIView(ListCRUDAPIView):
    serializer_class = TaxPayerSerializer
    user = None
    user_type = None

    def get(self, request, *args, **kwargs):
        # if user_type is TaxPayer then chnage to retrieve mode
        if self.user_type is TaxPayer:
            id = self.kwargs.get("id")
            if id is None:
                self.kwargs['id'] =self.user.id        
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        instance:TaxPayer =  serializer.save()
        if self.user_type is TaxAccountant:
            #adding curent user as taxaccountant for taxpayer
            instance.taxaccountants.add(self.user)
            instance.save()


    def get_queryset(self):
        self.user = self.request.user
        self.user_type = type(self.user)
        if  self.user_type is TaxAccountant:  
            qs = self.user.taxpayers.all()
            return qs#Getting only taxpayers related to TaxAccountant is user us TaxAccountant
        elif self.user_type is TaxPayer:
            # Making sure querying only taxpayer instead of all if user is taxpayer
            # This will also make sure tax payer has no access to other taxpayer data ,it throws 404 not found if id not matched with user id
            return TaxPayer.objects.filter(id=self.user.id)
        else:
            return TaxPayer.objects.all()

class TaxAccountantsAPIView(ListSingleModelMixin):
    serializer_class = TaxAccountantSerializer

    #Gets only Published posts
    def get_queryset(self):
        return TaxAccountant.objects.all()
