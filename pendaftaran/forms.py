from django import forms
from .models import Mahasiswa, Pendaftar
from .choices import JENIS_BERKAS_CHOICES

class PendaftaranForm(forms.ModelForm):
    class Meta:
        model = Mahasiswa
        fields = ['nama_lengkap', 'npm', 'email_aktif', 'strata', 'program_studi', 'periode_wisuda']

class UploadBerkasForm(forms.Form):
    jenis_berkas = forms.ChoiceField(
        choices=JENIS_BERKAS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

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
            'strata': forms.Select(attrs={'class': 'form-select'}),
            'program_studi': forms.Select(attrs={'class': 'form-select'}),
            'periode_wisuda': forms.Select(attrs={'class': 'form-select'}),
        }