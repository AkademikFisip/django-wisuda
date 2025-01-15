from django import forms
from .models import Mahasiswa, Pendaftar, Berkas
from .choices import JENIS_BERKAS_CHOICES, PROGRAM_STUDI_CHOICES, PERIODE_WISUDA_CHOICES, STRATA_CHOICES

class UploadBerkasForm(forms.ModelForm):
    class Meta:
        model = Berkas
        fields = ['jenis_berkas', 'file']
        widgets = {
            'jenis_berkas': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }

class UploadForm(forms.Form):
    jenis_berkas = forms.ChoiceField(choices=JENIS_BERKAS_CHOICES)
    file = forms.FileField()

class PendaftarForm(forms.ModelForm):
    class Meta:
        model = Pendaftar
        fields = [
            'nama_lengkap',
            'npm',
            'email_aktif',
            'nomor_wa',
            'strata',
            'program_studi',
            'periode_wisuda',
        ]
        widgets = {
            'nama_lengkap': forms.TextInput(attrs={'class': 'form-control'}),
            'npm': forms.TextInput(attrs={'class': 'form-control'}),
            'email_aktif': forms.EmailInput(attrs={'class': 'form-control'}),
            'nomor_wa': forms.TextInput(attrs={'class': 'form-control'}),
            'strata': forms.Select(choices=STRATA_CHOICES, attrs={'class': 'form-select'}),
            'program_studi': forms.Select(choices=PROGRAM_STUDI_CHOICES, attrs={'class': 'form-select'}),
            'periode_wisuda': forms.Select(choices=PERIODE_WISUDA_CHOICES, attrs={'class': 'form-select'}),
        }

class MahasiswaForm(forms.ModelForm):
    class Meta:
        model = Mahasiswa
        fields = [
            'nama_lengkap',
            'npm',
            'email_aktif',
            'nomor_wa',
            'strata',
            'program_studi',
            'periode_wisuda',
        ]
        widgets = {
            'nama_lengkap': forms.TextInput(attrs={'class': 'form-control'}),
            'npm': forms.TextInput(attrs={'class': 'form-control'}),
            'email_aktif': forms.EmailInput(attrs={'class': 'form-control'}),
            'nomor_wa': forms.TextInput(attrs={'class': 'form-control'}),
            'strata': forms.Select(choices=STRATA_CHOICES, attrs={'class': 'form-select'}),
            'program_studi': forms.Select(choices=PROGRAM_STUDI_CHOICES, attrs={'class': 'form-select'}),
            'periode_wisuda': forms.Select(choices=PERIODE_WISUDA_CHOICES, attrs={'class': 'form-select'}),
        }

    def clean_npm(self):
        npm = self.cleaned_data.get('npm')
        if not npm.isdigit():
            raise forms.ValidationError("NPM hanya boleh berisi angka.")
        return npm

    def clean_email_aktif(self):
        email = self.cleaned_data.get('email_aktif')
        if not email.endswith('@domain.edu'):
            raise forms.ValidationError("Gunakan email institusi dengan domain '@domain.edu'.")
        return email
