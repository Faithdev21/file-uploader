from rest_framework import status, mixins, viewsets
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from files.models import File
from api.serializers import FileSerializer
from api.tasks import process_file


class FileUploadView(mixins.CreateModelMixin,
                     GenericViewSet):
    """ViewSet for uploading files."""
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def perform_create(self, serializer):
        try:
            if not self.request.data.get('file'):
                return Response(
                    {"error": "Missing 'file' field in the request data."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            file_instance = serializer.save()
            process_file.delay(file_instance.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FileListView(mixins.ListModelMixin,
                   GenericViewSet):
    """ViewSet for reading files."""
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def list(self, request, *args, **kwargs):
        try:
            files = self.get_queryset()
            serializer = self.serializer_class(files, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
