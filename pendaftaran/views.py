from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from .forms import UploadBerkasForm
from .forms import PendaftaranForm
from .models import Berkas
from .models import Mahasiswa

# Create your views here.
def home(request):
    if request.method == 'POST':
        form = PendaftaranForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'pendaftaran/terima_kasih.html')
        else:
            form = PendaftaranForm()
            return render(request, 'pendaftaran/home.html', {'form': form})
            print(form.errors)  # Tambahkan ini untuk mencetak error
            return HttpResponse("Pastikan semua data terisi dengan benar.")

@login_required
def dashboard(request):
    if request.method == 'POST':
        jenis_berkas = request.POST.get('jenis_berkas')
        file = request.FILES.get('file')

        # Cek apakah berkas sudah ada
        berkas, created = Berkas.objects.get_or_create(user=request.user, jenis_berkas=jenis_berkas)
        berkas.file = file
        berkas.status = 'Menunggu Verifikasi'
        berkas.save()
        return redirect('dashboard')

    # Ambil semua berkas user
    berkas_user = {berkas.jenis_berkas: berkas for berkas in Berkas.objects.filter(user=request.user)}

    # Kirim data ke template
    form = UploadBerkasForm()
    return render(request, 'pendaftaran/dashboard.html', {
        'form': form,
        'berkas_user': berkas_user,
    })

def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')  # Nama Lengkap
        email = request.POST.get('email')         # Email Aktif
        password = request.POST.get('password')   # Password
        npm = request.POST.get('npm')             # NPM
        strata = request.POST.get('strata')       # Strata
        program_studi = request.POST.get('program_studi')  # Program Studi
        periode_wisuda = request.POST.get('periode_wisuda')  # Periode Wisuda

        # Validasi input form
        if not full_name or not email or not password or not npm or not strata or not program_studi or not periode_wisuda:
            messages.error(request, "Pastikan semua data terisi dengan benar.")
            return render(request, 'pendaftaran/register.html', {'form': form})


        # Buat user baru
        username = npm  # Gunakan NPM sebagai username
        if User.objects.filter(username=username).exists():
            return HttpResponseBadRequest("Akun dengan NPM ini sudah terdaftar.")
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = full_name
        user.save()

        # Simpan data tambahan di model Mahasiswa
        mahasiswa = Mahasiswa.objects.create(
            user=user,
            npm=npm,
            strata=strata,
            program_studi=program_studi,
            periode_wisuda=periode_wisuda
        )
        mahasiswa.save()

        # Login otomatis setelah register
        login(request, user)
        return redirect('dashboard')

    return render(request, 'pendaftaran/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validasi input kosong
        if not username or not password:
            messages.error(request, 'Username dan password harus diisi.')
            return render(request, 'pendaftaran/login.html')

        # Autentikasi pengguna
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect ke dashboard setelah login
        else:
            messages.error(request, 'Username atau password salah.')

    return render(request, 'pendaftaran/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Arahkan kembali ke halaman login setelah logout