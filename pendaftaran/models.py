from django.db import models
from django.contrib.auth.models import User
from .choices import JENIS_BERKAS_CHOICES, PROGRAM_STUDI_CHOICES, PERIODE_WISUDA_CHOICES, STRATA_CHOICES
from django.core.validators import RegexValidator
import os
from django.core.exceptions import ValidationError
import re

# Fungsi validasi password
def validate_password(value):
    if len(value) < 8:
        raise ValidationError('Password harus minimal 8 karakter.')
    if not re.search(r'[A-Za-z]', value):
        raise ValidationError('Password harus mengandung huruf.')
    if not re.search(r'\d', value):
        raise ValidationError('Password harus mengandung angka.')

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
    if ext.lower() not in valid_extensions:
        raise ValidationError('Hanya file PDF, JPG, JPEG, dan PNG yang diizinkan.')

def validate_file_size(value):
    limit = 5 * 1024 * 1024  # 5 MB
    if value.size > limit:
        raise ValidationError('Ukuran file tidak boleh lebih dari 5 MB.')
       
class Pendaftar(models.Model):
    nama = models.CharField(max_length=100)
    npm = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='NPM hanya boleh berisi angka.',
                code='invalid_npm'
            )
        ]
    )
    email = models.EmailField()
    strata = models.CharField(max_length=50, choices=STRATA_CHOICES)
    program_studi = models.CharField(max_length=100, choices=PROGRAM_STUDI_CHOICES)
    periode_wisuda = models.CharField(max_length=100, choices=PERIODE_WISUDA_CHOICES)
    password = models.CharField(
        max_length=128,
        validators=[validate_password]  # Validator custom digunakan di sini
    )

    def __str__(self):
        return self.nama

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
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='NPM hanya boleh berisi angka.',
                code='invalid_npm'
            )
        ]
    )
    email_aktif = models.EmailField()
    strata = models.CharField(max_length=50, choices=STRATA_CHOICES)
    program_studi = models.CharField(max_length=100, choices=PROGRAM_STUDI_CHOICES)
    periode_wisuda = models.CharField(max_length=100, choices=PERIODE_WISUDA_CHOICES)