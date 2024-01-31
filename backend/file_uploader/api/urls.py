from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import FileUploadView, FileListView


router = DefaultRouter()
router.register('upload', FileUploadView, basename='file-upload')
router.register('files', FileListView, basename='file-list')

urlpatterns = [
    path('', include(router.urls)),
]
