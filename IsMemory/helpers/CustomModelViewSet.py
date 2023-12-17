from rest_framework import viewsets

from IsMemory.helpers.CustomOptionsMetadata import CustomOptionsMetadata


class CustomModelViewSet(viewsets.ModelViewSet):
    serializer_list = {}
    metadata_class = CustomOptionsMetadata

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        return self.serializer_list.get(self.action, self.serializer_class)
