from django import forms
from .models import Mahasiswa
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