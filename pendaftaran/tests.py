
from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from .models import Pendaftar
from .views import home, dashboard

# Model Tests
class PendaftarModelTest(TestCase):
    def test_create_pendaftar(self):
        # Gunakan field yang sesuai dengan model Pendaftar
        pendaftar = Pendaftar.objects.create(
            nama="John Doe",  # Ganti nama_lengkap menjadi nama
            npm="123456789",  # Pastikan sesuai dengan tipe data
            email="johndoe@example.com",  # Gunakan email field
            strata="S1",  # Pilihan strata yang valid
            program_studi="ilmu_komunikasi",  # Pilihan program_studi yang valid
            periode_wisuda="periode_I"  # Pilihan periode_wisuda yang valid
        )
        # Uji apakah data berhasil disimpan dengan benar
        self.assertEqual(pendaftar.nama, "John Doe")
        self.assertEqual(pendaftar.npm, "123456789")

# View Tests
class HomeViewTest(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get(reverse('pendaftaran:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_template(self):
        response = self.client.get(reverse('pendaftaran:home'))
        self.assertTemplateUsed(response, 'pendaftaran/home.html')

class DashboardViewTest(TestCase):
    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('pendaftaran:dashboard'))
        self.assertNotEqual(response.status_code, 200)

# URL Tests
class UrlsTest(SimpleTestCase):
    def test_home_url_resolves(self):
        url = reverse('pendaftaran:home')
        self.assertEqual(resolve(url).func, home)

    def test_dashboard_url_resolves(self):
        url = reverse('pendaftaran:dashboard')
        self.assertEqual(resolve(url).func, dashboard)
