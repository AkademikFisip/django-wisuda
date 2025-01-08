
from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from .models import Pendaftar
from .views import home, dashboard

# Model Tests
class PendaftarModelTest(TestCase):
    def test_create_pendaftar(self):
        pendaftar = Pendaftar.objects.create(
            nama_lengkap="John Doe",
            npm="123456789",
            email="johndoe@example.com",
            password="hashedpassword",
            strata="S1",
            program_studi="ilmu_komunikasi",
            periode_wisuda="periode_I"
        )
        self.assertEqual(pendaftar.nama_lengkap, "John Doe")
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
