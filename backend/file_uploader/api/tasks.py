from celery import shared_task
from files.models import File
import magic
from PIL import Image
import textract
import fitz
from pydub import AudioSegment
import cv2


@shared_task
def process_file(file_id):
    try:
        file_instance = File.objects.get(pk=file_id)
        mime = magic.Magic()
        file_type = mime.from_buffer(file_instance.file.read(1024))

        if 'image' in file_type:
            process_image(file_instance)
        elif 'text' in file_type:
            process_text(file_instance)
        elif 'pdf' in file_type:
            process_pdf(file_instance)
        elif 'audio' in file_type:
            process_audio(file_instance)
        elif 'video' in file_type:
            process_video(file_instance)
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
    """Обработка PDF-файла (пример: извлечение текста)."""
    try:
        with fitz.open(file_instance.file.path) as pdf_doc:
            text = ""
            for page_num in range(pdf_doc.page_count):
                page = pdf_doc[page_num]
                text += page.get_text()
            print(f"Extracted text from PDF: {text}")
    except Exception as e:
        raise ValueError(f"Error processing PDF: {e}")


def process_audio(file_instance):
    """Обработка аудиофайла (пример: конвертация в MP3)."""
    try:
        audio = AudioSegment.from_file(file_instance.file.path)
        audio.export(file_instance.file.path, format="mp3")
        print("Audio file processed")
    except Exception as e:
        raise ValueError(f"Error processing audio: {e}")


def process_video(file_instance):
    """Обработка видеофайла (пример: извлечение кадров)."""
    try:
        cap = cv2.VideoCapture(file_instance.file.path)
        success, image = cap.read()

        if success:
            cv2.imwrite(file_instance.file.path + ".jpg", image)
            print("Video file processed")
        else:
            raise ValueError("Error processing video")
    except Exception as e:
        raise ValueError(f"Error processing video: {e}")
