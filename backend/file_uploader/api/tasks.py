from celery import shared_task
from files.models import File


@shared_task
def process_file(file_id):
    file_instance = File.objects.get(pk=file_id)
    file_instance.processed = True
    file_instance.save()
