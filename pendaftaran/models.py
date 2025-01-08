from django.db import models
from django.contrib.auth.models import User
from .choices import JENIS_BERKAS_CHOICES
from django.core.validators import RegexValidator
import os
from django.core.exceptions import ValidationError

class Pendaftar(models.Model):
    nama = models.CharField(max_length=100)
    npm = models.CharField(max_length=15, default="00000000")
    email = models.EmailField()
    strata = models.CharField(max_length=50, choices=JENIS_BERKAS_CHOICES)
    program_studi = models.CharField(max_length=100, choices=JENIS_BERKAS_CHOICES)
    periode_wisuda = models.CharField(max_length=100, default="2025-01", choices=JENIS_BERKAS_CHOICES)

    def __str__(self):
        return self.nama

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
    if ext.lower() not in valid_extensions:
        raise ValidationError('Hanya file PDF, JPG, JPEG, dan PNG yang diizinkan.')

def validate_file_size(value):
    limit = 5 * 1024 * 1024  # 5 MB
    if value.size > limit:
        raise ValidationError('Ukuran file tidak boleh lebih dari 5 MB.')

class Berkas(models.Model):
    jenis_berkas = models.CharField(max_length=100, choices=JENIS_BERKAS_CHOICES)
    file = models.FileField(
        upload_to='berkas/',
        validators=[validate_file_extension, validate_file_size]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Mahasiswa(models.Model):
    nama_lengkap = models.CharField(max_length=100)
    npm = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='NPM hanya boleh berisi angka.',
                code='invalid_npm'
            )
        ]
    )
    email_aktif = models.EmailField()
    strata = models.CharField(max_length=50, choices=JENIS_BERKAS_CHOICES)
    program_studi = models.CharField(max_length=100, choices=JENIS_BERKAS_CHOICES)
    periode_wisuda = models.CharField(max_length=100, choices=JENIS_BERKAS_CHOICES)