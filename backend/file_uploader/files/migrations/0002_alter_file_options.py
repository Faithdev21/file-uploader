# Generated by Django 3.2 on 2024-01-31 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='file',
            options={'ordering': ('id',), 'verbose_name': 'File', 'verbose_name_plural': 'Files'},
        ),
    ]