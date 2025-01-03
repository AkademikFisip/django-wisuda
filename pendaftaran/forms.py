from django import forms
from .models import Berkas
from .models import Mahasiswa

class PendaftaranForm(forms.ModelForm):
    class Meta:
        model = Mahasiswa
        fields = ['nama_lengkap', 'npm', 'email_aktif', 'strata', 'program_studi', 'periode_wisuda']

class UploadBerkasForm(forms.ModelForm):
    class Meta:
        model = Berkas
        fields = ['jenis_berkas', 'file']
