from django.db import models


class File(models.Model):
    """File model."""
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(
        'Publication data',
        db_index=True,
        auto_now_add=True
    )
    processed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'
        ordering = ('id',)

    def __str__(self):
        return self.file.name
