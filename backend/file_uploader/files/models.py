from django.db import models
from django.utils import timezone


class File(models.Model):
    """File model."""
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(
        'Publication date',
        db_index=True,
        default=timezone.now
    )
    processed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'
        ordering = ('-id',)

    def __str__(self):
        return self.file.name
