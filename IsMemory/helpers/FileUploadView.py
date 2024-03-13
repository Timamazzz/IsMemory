import os
from datetime import datetime
from django.core.files.storage import default_storage
from django.utils.text import slugify, get_valid_filename
from rest_framework import status, serializers
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
import json


class FileSerializer(serializers.Serializer):
    url = serializers.SerializerMethodField()
    name = serializers.CharField()
    original_name = serializers.CharField()
    date = serializers.DateTimeField()
    extension = serializers.CharField()

    def get_url(self, obj):
        return default_storage.url(obj['name'])

    def create(self, validated_data):
        file_list = validated_data['file']
        response_files = []

        for file_item in file_list:
            original_name = file_item.name
            file_extension = os.path.splitext(original_name)[-1].lower()

            slug_field_name = slugify(original_name)
            file_name = get_valid_filename(slug_field_name)
            file_name = default_storage.save(file_name, file_item)

            response_files.append({
                "name": file_name,
                "original_name": original_name,
                "date": datetime.now().isoformat(),
                "extension": file_extension,
            })

        return self.to_representation(response_files)


class FileUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        print("request", request.__dict__)
        print("files", request.FILES)
        print("get files", request.FILES.getlist('file'))
        serializer = FileSerializer(data={'file': request.FILES.getlist('file')}, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
