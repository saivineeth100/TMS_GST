
from rest_framework import generics, status, mixins
from rest_framework.response import Response

class CRUDAPIView(generics.CreateAPIView,generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "id"

    def get_queryset(self):
        return self.model.objects.all()

    
    def get_serializer(self, *args, **kwargs):
        """ 
        if an array is passed, set serializer to many 
        Enables to create Multiple items 
        """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        response.data = {'status': 'Deleted successfully'}
        return response


class ListModelMixin(mixins.ListModelMixin):
    
    def get(self, request, *args, **kwargs):
        urlparams = list(self.kwargs.keys())
        if len(urlparams) > 0:
            self.lookup_field = urlparams[0]
            return self.retrieve(request, *args, **kwargs)
        else:
            maxobjectsperpage = self.request.query_params.get("max",None)
            if self.paginator is not None:
                self.paginator.page_size = maxobjectsperpage if maxobjectsperpage is not None else self.paginator.page_size
            return self.list(request, *args, **kwargs)

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        # To get Totalpages count
        response.data['total_pages'] = self.paginator.page.paginator.num_pages
        return response

class ListCRUDAPIView(ListModelMixin, CRUDAPIView):
    pass

#Able to get single Object or List    
class ListSingleModelMixin(ListModelMixin,mixins.RetrieveModelMixin,generics.GenericAPIView):
    pass

