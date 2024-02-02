import os

import fitz
import magic
import textract
from celery import shared_task
from PIL import Image

from files.models import File


@shared_task
def process_file(file_id):
    try:
        file_instance = File.objects.get(pk=file_id)
        mime = magic.Magic()
        file_type = mime.from_buffer(file_instance.file.read(1024))

        if 'image' in file_type.lower():
            process_image(file_instance)
        elif 'text' in file_type.lower():
            process_text(file_instance)
        elif 'pdf' in file_type.lower():
            process_pdf(file_instance)
        else:
            raise ValueError("Unsupported file type")

        file_instance.processed = True
        file_instance.save()

    except File.DoesNotExist:
        raise ValueError(f"File with id {file_id} does not exist.")
    except Exception as e:
        raise ValueError(f"An error occurred: {e}")


def process_image(file_instance):
    """Обработка изображения (пример: изменение размера)."""
    try:
        with Image.open(file_instance.file.path) as img:
            resized_img = img.resize((100, 100))
            resized_img.save(file_instance.file.path)
    except Exception as e:
        raise ValueError(f"Error processing image: {e}")


def process_text(file_instance):
    """Обработка текстового файла (пример: извлечение текста)."""
    try:
        text = textract.process(file_instance.file.path)
        print(f"Extracted text: {text}")
    except Exception as e:
        raise ValueError(f"Error processing text: {e}")


def process_pdf(file_instance):
    """Обработка PDF-файла (пример: извлечение текста в txt файл)."""
    try:
        with fitz.open(file_instance.file.path) as pdf_doc:
            text = ""
            for page_num in range(pdf_doc.page_count):
                page = pdf_doc[page_num]
                text += page.get_text()

            base_name, ext = os.path.splitext(file_instance.file.name)
            text_file_name = base_name + "_text.txt"
            text_file_path = os.path.join("", text_file_name)

            with open(text_file_path, "w", encoding="utf-8") as text_file:
                text_file.write(text)

            print(f"Extracted text from PDF and saved to: {text_file_path}")
    except Exception as e:
        raise ValueError(f"Error processing PDF: {e}")
