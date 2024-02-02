from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import FileListView, FileUploadView

router = DefaultRouter()
router.register('upload', FileUploadView, basename='file-upload')
router.register('files', FileListView, basename='file-list')

urlpatterns = [
    path('', include(router.urls)),
]
