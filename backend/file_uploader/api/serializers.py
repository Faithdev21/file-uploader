from typing import Tuple

from rest_framework import serializers

from files.models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields: Tuple[str, ...] = ('id', 'file', 'uploaded_at', 'processed',)
