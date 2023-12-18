import os
from datetime import datetime

from django.core.files.storage import default_storage
from django.utils.text import slugify, get_valid_filename
from rest_framework import decorators, serializers, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response


class UploadMultipleSerializer(serializers.Serializer):
    file = serializers.ListField(
        child=serializers.FileField(required=True, allow_empty_file=False))

    def save(self):
        file_list = self.validated_data.get('file')

        list_saved = []

        for file_item in file_list:
            file_name = default_storage.save(file_item.name, file_item)
            list_saved.append(file_name)

        request = self.context.get('request')

        response_files = []

        for file_name in list_saved:
            if request is not None:
                response_files.append(request.build_absolute_uri(default_storage.url(file_name)))
            else:
                response_files.append(default_storage.url(file_name))

        return response_files


class UploadMultipleFileImageMixin:
    @decorators.action(detail=False, methods=['post'],
                       serializer_class=UploadMultipleSerializer,
                       parser_classes=[MultiPartParser, ])
    def upload(self, request, *args, **kwargs):
        file_list = request.FILES.getlist('file')

        response_files = []

        for file_item in file_list:
            original_name = file_item.name
            file_extension = os.path.splitext(original_name)[-1].lower()

            slugified_name = slugify(original_name)

            file_name = get_valid_filename(slugified_name)
            file_name = default_storage.save(file_name, file_item)

            file_url = default_storage.url(file_name)
            response_files.append({
                "url": file_url,
                "name": file_name,
                "original_name": original_name,
                "date": datetime.now().isoformat(),
                "extension": file_extension,
            })

        return Response(response_files, status=status.HTTP_200_OK)
