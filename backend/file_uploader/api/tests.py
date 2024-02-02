from collections import OrderedDict
from datetime import datetime
from http import HTTPStatus
from time import sleep
from unittest.mock import patch, mock_open

from celery.result import AsyncResult
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from files.models import File

from api.tasks import process_file, process_pdf, process_text, process_image


class FileUploadingTest(TestCase):
    def test_file_uploading(self):
        file_content = "Hello, this is a test file."
        file = SimpleUploadedFile("test_file.txt", file_content.encode())
        file_obj = File.objects.create(file=file, processed=True)
        process_file.delay(file_obj.id)
        file_obj.refresh_from_db()
        self.assertTrue(file_obj.processed)


class ApiPagesURLTests(APITestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_files_url_exists_at_desired_location(self):
        response = self.guest_client.get('/api/files/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_url_get_requests(self):
        response_get = self.guest_client.get('/api/upload/')
        self.assertEqual(response_get.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_upload_url_post_requests(self):
        file_content = "Hello, this is a test file."
        file = SimpleUploadedFile("test_file.txt", file_content.encode())
        response_post = self.guest_client.post('/api/upload/', {'file': file})

        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)

    def test_missing_file_field(self):
        response = self.client.post('/api/upload/', {'other_field': 'value'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class FileViewTests(TestCase):
    def test_file_created(self):
        file = File.objects.create(uploaded_at=timezone.now())
        self.assertIsNotNone(file)

    def test_file_list_view(self):
        file = File.objects.create(
            file='file1.txt',
            uploaded_at=timezone.now(),
            processed=True
        )

        response = self.client.get('/api/files/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = [
            OrderedDict([
                ('id', file.id),
                ('file', f'/{file.file.name}'),
                ('uploaded_at', timezone.localtime(file.uploaded_at).isoformat()),
                ('processed', True)
            ])
        ]
        self.assertEqual(response.data, expected_data)


class FileModelTests(TestCase):
    def test_str(self):
        file = File.objects.create(file='test.txt')
        self.assertEqual(str(file), 'test.txt')

    def test_upload_to(self):
        file = File.objects.create(file='test.txt')
        self.assertEqual(file.file.field.upload_to, 'uploads/')

    def test_processed(self):
        file = File.objects.create(file='test.txt')
        self.assertFalse(file.processed)


class ProcessImageTest(TestCase):
    @patch('api.tasks.Image.open')
    def test_process_image(self, mock_image_open):
        file_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
        file = SimpleUploadedFile("test_image.png", file_content)
        file_obj = File.objects.create(file=file)

        process_file(file_obj.pk)

        mock_image_open.assert_called_once_with(file_obj.file.path)


class ProcessTextTest(TestCase):
    @patch('api.tasks.textract.process')
    def test_process_text(self, mock_textract_process):
        file_content = "This is a sample text file."
        file = SimpleUploadedFile("test_text.txt", file_content.encode())
        file_obj = File.objects.create(file=file)

        process_file(file_obj.pk)

        mock_textract_process.assert_called_once_with(file_obj.file.path)


class ProcessPDFTest(TestCase):
    @patch('api.tasks.fitz.open')
    @patch('api.tasks.open', mock_open(), create=True)
    def test_process_pdf(self, mock_fitz_open):
        file_content = b'%PDF-1.5\n\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n\n3 0 obj\n<< /Type /Page /Parent 2 0 R >>\nendobj\n\nxref\n0 4\n0000000000 65535 f \n0000000010 00000 n \n0000000060 00000 n \n0000000125 00000 n \n0000000173 00000 n \ntrailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n217\n%%EOF'
        file = SimpleUploadedFile("test_pdf.pdf", file_content)
        file_obj = File.objects.create(file=file)
        process_file(file_obj.pk)

        mock_fitz_open.assert_called_once_with(file_obj.file.path)
