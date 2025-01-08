from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseBadRequest
from .forms import UploadBerkasForm, PendaftaranForm
from .models import Berkas, Pendaftar

def home(request):
    if request.method == 'POST':
        form = PendaftaranForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'pendaftaran/terima_kasih.html')
        else:
            # Render ulang dengan data error yang sudah ada
            return render(request, 'pendaftaran/home.html', {'form': form})
    else:
        form = PendaftaranForm()
        return render(request, 'pendaftaran/home.html', {'form': form})
    
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validasi input
        if not username or not email or not password:
            messages.error(request, 'Semua field wajib diisi.')
            return redirect('pendaftaran:register')

        # Cek apakah email sudah digunakan
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah digunakan.')
            return redirect('pendaftaran:register')

        # Buat pengguna baru
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, 'Akun berhasil dibuat. Silakan login.')
        return redirect('pendaftaran:login')

    return render(request, 'pendaftaran/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('pendaftaran:dashboard')  # Ubah sesuai dengan nama URL dashboard Anda
        else:
            messages.error(request, 'Username atau password salah.')
    return render(request, 'pendaftaran/login.html')

@login_required
def dashboard(request):
    if request.method == 'POST':
        jenis_berkas = request.POST.get('jenis_berkas')
        file = request.FILES.get('file')

        # Validasi file sebelum menyimpan
        if not file or not jenis_berkas:
            return HttpResponseBadRequest("Jenis berkas atau file tidak valid.")

        # Cek apakah berkas sudah ada atau buat baru
        berkas, created = Berkas.objects.get_or_create(user=request.user, jenis_berkas=jenis_berkas)
        berkas.file = file
        berkas.status = 'Menunggu Verifikasi'
        berkas.save()

        # Berikan feedback ke pengguna
        return redirect('dashboard')

    # Query data mahasiswa
    mahasiswa = User.objects.get(username=request.user.username)

    # Ambil semua berkas yang dimiliki pengguna
    berkas_list = Berkas.objects.filter(user=request.user)
    return render(request, 'pendaftaran/dashboard.html', {'mahasiswa': mahasiswa, 'berkas_list': berkas_list})

from django.shortcuts import redirect
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('pendaftaran/login.html')
