from django.db import models
from django.contrib.auth.models import User

JENIS_BERKAS_CHOICES = [
    ('foto', 'Foto hitam putih dengan latar putih'),
    ('ktm', 'Kartu Tanda Mahasiswa'),
    ('skpi', 'Surat Keterangan Pendamping Ijazah'),
    ('ukt', 'Bukti Pembayaran UKT'),
    ('judul', 'Judul dan Pengesahan TA/Skripsi/Disertasi'),
    ('usul', 'Berita Acara Seminar Usul'),
    ('ujian', 'Berita Acara Ujian TA/Skripsi/Disertasi'),
    ('tatib', 'Surat Pernyataan Tata Tertib Wisudawan'),
    ('ept_toefl', 'Sertifikat EPT/Toefl'),
    ('bebas_perpus_ruang_baca', 'Bukti Bebas Pinjam Ruang Baca FISIP dan UPT Perpustakaan Unila'),
    ('upload_sebar', 'Bukti Upload dan Sebar'),
    ('ijazah', 'Ijasah SLTA/D3/S1/S2'),
    ('sk_pembimbing', 'SK Pembimbing'),
    ('sk_penguji', 'SK Penguji'),
]

PROGRAM_STUDI_CHOICES = [
    ('sosiologi', 'Sosiologi'), 
    ('ilmu_pemerintahan', 'Ilmu Pemerintahan'), 
    ('ilmu_komunikasi', 'Ilmu Komunikasi'), 
    ('administrasi_negara', 'Administrasi Negara'), 
    ('ilmu_administrasi_bisnis', 'Ilmu Administrasi Bisnis'), 
    ('hubungan_internasional', 'Hubungan Internasional'), 
    ('administrasi_perkantoran', 'Administrasi Perkantoran'), 
    ('hubungan_masyarakat', 'Hubungan Masyarakat'), 
    ('perpustakaan', 'Perpustakaan'), 
    ('studi_pembangunan', 'Studi Pembangunan')
]

PERIODE_WISUDA = [
    ('periode_I', 'Periode I'),
    ('periode_II', 'Periode II'),
    ('periode_III', 'Periode III'),
    ('periode_IV', 'Periode IV'),
    ('periode_V', 'Periode V'),
    ('periode_VI', 'Periode VI'),
    ('periode_VII', 'Periode VII'),
]

STRATA = [
    ('D3', 'D3'), 
    ('S1', 'S1'), 
    ('S2', 'S2'), 
    ('S3', 'S3')
]

from django.db import models

class Pendaftar(models.Model):
    nama = models.CharField(max_length=100)
    npm = models.CharField(max_length=20)
    email = models.EmailField()
    strata = models.CharField(max_length=10, choices=STRATA)
    program_studi = models.CharField(max_length=50, choices=PROGRAM_STUDI_CHOICES)
    periode_wisuda = models.CharField(max_length=50, choices=PERIODE_WISUDA)

    def __str__(self):
        return self.nama

class Berkas(models.Model):
    jenis_berkas = models.CharField(max_length=100, choices=JENIS_BERKAS_CHOICES)
    file = models.FileField(upload_to='berkas/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return dict(JENIS_BERKAS_CHOICES).get(self.jenis_berkas, "Unknown")
    
class Mahasiswa(models.Model):
    nama_lengkap = models.CharField(max_length=100)
    npm = models.CharField(max_length=15)
    email_aktif = models.EmailField()
    strata = models.CharField(max_length=10, choices=STRATA)
    program_studi = models.CharField(max_length=50, choices=PROGRAM_STUDI_CHOICES)
    periode_wisuda = models.CharField(max_length=50, choices=PERIODE_WISUDA)

    def __str__(self):
        return self.nama_lengkap