from rest_framework import status, mixins, viewsets
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from files.models import File
from api.serializers import FileSerializer
from api.tasks import process_file


class FileUploadView(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def perform_create(self, serializer):
        file_instance = serializer.save()
        process_file.delay(file_instance.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FileListView(mixins.ListModelMixin,
                   GenericViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
