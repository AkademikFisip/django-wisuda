from django.db import models
from django.contrib.auth.models import User
from .choices import JENIS_BERKAS_CHOICES, PROGRAM_STUDI_CHOICES, PERIODE_WISUDA_CHOICES, STRATA_CHOICES
from django.core.validators import RegexValidator
import os, re
from django.core.exceptions import ValidationError
from django.utils.timezone import now

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
       
def get_default_user():
    user = User.objects.first()  # Pastikan ada user pertama
    return user.id if user else None  # Kembalikan ID User, bukan objek User

class Pendaftar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=get_default_user)
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
    nomor_wa = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{10,15}$',
                message='Nomor WA harus berupa angka, minimal 10 digit.'
            )
        ]
    )

    strata = models.CharField(max_length=50, choices=STRATA_CHOICES)
    program_studi = models.CharField(max_length=50, choices=PROGRAM_STUDI_CHOICES)
    periode_wisuda = models.CharField(max_length=50, choices=PERIODE_WISUDA_CHOICES)

    def __str__(self):
        return self.nama_lengkap

class Berkas(models.Model):
    pendaftar = models.ForeignKey(Pendaftar, on_delete=models.CASCADE, related_name="berkas_set", default=get_default_user)
    jenis_berkas = models.CharField(max_length=50, choices=JENIS_BERKAS_CHOICES)
    file = models.FileField(
        upload_to='berkas/',
        validators=[validate_file_extension, validate_file_size])
    def __str__(self):
        return f"{self.user.username} - {self.jenis_berkas}"

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
    if ext not in valid_extensions:
        raise ValidationError("Hanya file dengan format PDF, JPG, JPEG, atau PNG yang diizinkan.")
    
class Mahasiswa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
    email_aktif = models.EmailField(max_length=100)
    nomor_wa = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{10,15}$',
                message='Nomor WA harus berupa angka, minimal 10 digit.'
            )
        ]
    )
    strata = models.CharField(max_length=50, choices=STRATA_CHOICES)
    program_studi = models.CharField(max_length=50, choices=PROGRAM_STUDI_CHOICES)
    periode_wisuda = models.CharField(max_length=50, choices=PERIODE_WISUDA_CHOICES)

    def __str__(self):
       return self.nama_lengkap